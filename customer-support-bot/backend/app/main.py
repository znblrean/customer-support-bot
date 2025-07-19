<<<<<<< HEAD
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
=======
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.database import DatabaseService
from app.agents.support_agent import SupportAgent
from app.utils.logger import setup_logger
from dotenv import load_dotenv


load_dotenv()
logger = setup_logger()

app = FastAPI(
    title="Customer Support Bot API",
    description="API for AI-powered customer support chatbot",
    version="1.0.0"
)
>>>>>>> cfb62a60 (new pip install langsmith langchain openai)

# تنظیمات CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
<<<<<<< HEAD
=======
    allow_credentials=True,
>>>>>>> cfb62a60 (new pip install langsmith langchain openai)
    allow_methods=["*"],
    allow_headers=["*"],
)

<<<<<<< HEAD
@app.get("/")
async def root():
    return {"message": "خوش آمدید به سامانه پشتیبانی"}
=======
# راه‌اندازی سرویس‌ها
db_service = DatabaseService()
support_agent = SupportAgent(db_service)

@app.on_event("startup")
async def startup_event():
    await db_service.initialize()
    logger.info("Application started successfully")

@app.post("/api/conversation")
async def handle_conversation(user_input: str, user_id: str, session_id: str = None):
    """
    پردازش پیام کاربر و تولید پاسخ
    """
    try:
        response = await support_agent.process_message(
            user_input=user_input,
            user_id=user_id,
            session_id=session_id
        )
        return {
            "response": response["message"],
            "session_id": response["session_id"],
            "metadata": response.get("metadata", {})
        }
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
>>>>>>> cfb62a60 (new pip install langsmith langchain openai)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)