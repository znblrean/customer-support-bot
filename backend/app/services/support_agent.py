from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from app.utils.tracing import trace_chain

class SupportAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4-1106-preview",
            temperature=0.7
        )
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", "شما یک چت‌بات پشتیبانی مشتریان هستید. به سوالات مشتریان پاسخ می‌دهید."),
            ("human", "{user_input}")
        ])
    
    @trace_chain
    def generate_response(self, user_input: str):
        chain = self.prompt_template | self.llm
        return chain.invoke({"user_input": user_input}).content

from app.utils.langsmith import LangSmithManager

langsmith = LangSmithManager()

class SupportAgent:
    @langsmith.trace
    def generate_response(self, user_input: str):
        # منطق تولید پاسخ
        return response