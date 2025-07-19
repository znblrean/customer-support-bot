import os
import json
import logging
from typing import Dict, Optional
from openai import OpenAI
from app.services.database import DatabaseService
from app.utils.security import sanitize_input
from app.utils.logger import logger

class SupportAgent:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.system_prompt = """
        شما یک چت‌بات پشتیبانی مشتریان هستید. وظایف شما:
        1. پاسخ به سوالات متداول درباره محصولات و خدمات
        2. کمک به پیگیری سفارشات
        3. راهنمایی برای حل مشکلات فنی
        4. تشخیص احساسات کاربر و پاسخ مناسب
        5. در صورت نیاز انتقال به اپراتور انسانی
        
        نکات مهم:
        - همیشه مودب و مفید باشید
        - از اصطلاحات فنی پیچیده اجتناب کنید
        - برای سوالات تخصصی به اپراتور انسانی ارجاع دهید
        - در صورت تشخیص نارضایتی کاربر، اولویت را بالا ببرید
        """
        
        # تنظیمات مدل
        self.model_config = {
            "default": "gpt-3.5-turbo",
            "high_priority": "gpt-4",
            "temperature": 0.7,
            "max_tokens": 500
        }

    async def process_message(self, user_input: str, user_id: str, session_id: Optional[str] = None) -> Dict:
        """پردازش پیام کاربر و تولید پاسخ"""
        try:
            # پاکسازی ورودی کاربر
            sanitized_input = sanitize_input(user_input)
            
            # بازیابی تاریخچه مکالمه
            conversation_history = await self._get_conversation_history(user_id, session_id)
            
            # تشخیص احساسات
            sentiment = self._detect_sentiment(sanitized_input)
            
            # تشخیص قصد کاربر
            intent = await self._detect_intent(sanitized_input)
            
            # تولید پاسخ
            response = await self._generate_response(
                user_input=sanitized_input,
                history=conversation_history,
                sentiment=sentiment,
                intent=intent
            )
            
            # ذخیره مکالمه
            await self._store_conversation(
                user_id=user_id,
                session_id=session_id or response["session_id"],
                user_input=sanitized_input,
                bot_response=response["message"],
                sentiment=sentiment,
                intent=intent
            )
            
            return response
        except Exception as e:
            logger.error(f"Error in process_message: {str(e)}")
            raise

    async def _get_conversation_history(self, user_id: str, session_id: Optional[str]) -> list:
        """بازیابی تاریخچه مکالمه از Redis یا دیتابیس"""
        history = []
        
        # اول از Redis بررسی می‌کنیم
        if session_id and self.db_service.redis:
            redis_key = f"conv:{user_id}:{session_id}"
            cached_history = self.db_service.redis.get(redis_key)
            if cached_history:
                return json.loads(cached_history)
        
        # اگر در Redis نبود، از دیتابیس می‌خوانیم
        async with await self.db_service.get_session() as session:
            result = await session.execute(
                select(Conversation)
                .where(Conversation.user_id == user_id)
                .order_by(Conversation.created_at.desc())
                .limit(5)
            )
            history = [{
                "user": conv.user_message,
                "bot": conv.bot_response
            } for conv in result.scalars()]
        
        return history

    def _detect_sentiment(self, text: str) -> str:
        """تشخیص احساسات متن با استفاده از مدل کوچکتر"""
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "فقط یکی از این برچسب‌ها را برگردان: positive, neutral, negative"
                }, {
                    "role": "user",
                    "content": text
                }],
                temperature=0.2,
                max_tokens=10
            )
            return response.choices[0].message.content.lower()
        except Exception as e:
            logger.warning(f"Sentiment detection failed: {str(e)}")
            return "neutral"

    async def _detect_intent(self, text: str) -> str:
        """تشخیص قصد کاربر"""
        intents = {
            "product_info": ["قیمت", "موجودی", "ویژگی", "مشخصات"],
            "order_status": ["پیگیری", "سفارش", "کد رهگیری"],
            "technical_support": ["نصب", "خطا", "ارور", "مشکل"],
            "complaint": ["شکایت", "ناراضی", "اعتراض"],
            "human_agent": ["انسان", "مسئول", "پشتیبان"]
        }
        
        # ابتدا بررسی ساده
        for intent, keywords in intents.items():
            if any(keyword in text for keyword in keywords):
                return intent
                
        # اگر تشخیص داده نشد، از مدل استفاده می‌کنیم
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system",
                    "content": "فقط نام intent را از بین گزینه‌ها برگردان: product_info, order_status, technical_support, complaint, human_agent, other"
                }, {
                    "role": "user",
                    "content": text
                }],
                temperature=0.3,
                max_tokens=20
            )
            return response.choices[0].message.content.lower()
        except Exception as e:
            logger.warning(f"Intent detection failed: {str(e)}")
            return "other"

    async def _generate_response(self, user_input: str, history: list, sentiment: str, intent: str) -> Dict:
        """تولید پاسخ با استفاده از مدل زبانی"""
        try:
            # انتخاب مدل بر اساس اولویت
            model = self.model_config["high_priority"] if sentiment == "negative" else self.model_config["default"]
            
            # ساخت محتوای مکالمه
            messages = [{"role": "system", "content": self.system_prompt}]
            
            # اضافه کردن تاریخچه مکالمه
            for item in history:
                messages.append({"role": "user", "content": item["user"]})
                messages.append({"role": "assistant", "content": item["bot"]})
            
            # اضافه کردن پیام فعلی کاربر
            messages.append({"role": "user", "content": user_input})
            
            # تولید پاسخ
            response = self.openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=self.model_config["temperature"],
                max_tokens=self.model_config["max_tokens"]
            )
            
            # پردازش پاسخ
            bot_response = response.choices[0].message.content
            
            # بررسی نیاز به انتقال به اپراتور انسانی
            if intent == "human_agent" or sentiment == "negative":
                bot_response += "\n\nدر حال اتصال شما به پشتیبان انسانی..."
            
            return {
                "message": bot_response,
                "session_id": self._generate_session_id(),
                "metadata": {
                    "model": model,
                    "sentiment": sentiment,
                    "intent": intent
                }
            }
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return {
                "message": "متأسفم، در پردازش درخواست شما مشکلی پیش آمده. لطفاً稍后再试.",
                "session_id": self._generate_session_id(),
                "metadata": {"error": str(e)}
            }

    def _generate_session_id(self) -> str:
        """تولید شناسه یکتا برای جلسه مکالمه"""
        import uuid
        return str(uuid.uuid4())

    async def _store_conversation(self, **kwargs):
        """ذخیره مکالمه در دیتابیس و Redis"""
        # ذخیره در PostgreSQL
        await self.db_service.store_conversation({
            "user_id": kwargs["user_id"],
            "session_id": kwargs["session_id"],
            "user_message": kwargs["user_input"],
            "bot_response": kwargs["bot_response"],
            "sentiment": kwargs["sentiment"],
            "intent": kwargs["intent"],
            "metadata": {
                "source": "chatbot",
                "priority": "high" if kwargs["sentiment"] == "negative" else "normal"
            }
        })
        
        # ذخیره در Redis برای دسترسی سریع
        if self.db_service.redis:
            redis_key = f"conv:{kwargs['user_id']}:{kwargs['session_id']}"
            conversation = {
                "user": kwargs["user_input"],
                "bot": kwargs["bot_response"],
                "timestamp": str(datetime.utcnow())
            }
            self.db_service.redis.setex(redis_key, 3600, json.dumps(conversation))

from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import ChatPromptTemplate
from app.services.conversation_service import ConversationService

class SupportAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=0.7,
            model="gpt-4",
            streaming=True
        )
        self.conversation_service = ConversationService()
        
        self.prompt = ChatPromptTemplate.from_template(
            """You are a customer support agent. Respond to: {user_input}"""
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=self.prompt
        )
    
    async def respond(self, user_input: str):
        response = await self.chain.arun(
            user_input=user_input,
            callbacks=[self.conversation_service.callback_manager]
        )
        
        await self.conversation_service.log_conversation(user_input, response)
        return response