import os
from langsmith import Client
from langchain.callbacks.manager import tracing_v2_enabled

class LangSmithManager:
    def __init__(self):
        self.api_key = os.getenv("LANGCHAIN_API_KEY")
        self.project_id = os.getenv("LANGCHAIN_PROJECT_ID")
        self.client = Client(api_key=self.api_key)
    
    def trace(self, func):
        """دکوراتور برای ردیابی عملکرد توابع"""
        def wrapper(*args, **kwargs):
            with tracing_v2_enabled(
                project_name=self.project_id,
                tags=["customer-support", "persian"]
            ):
                return func(*args, **kwargs)
        return wrapper
    
    def log_feedback(self, run_id: str, score: int, comment: str = ""):
        """ثبت بازخورد برای اجراهای خاص"""
        self.client.create_feedback(
            run_id=run_id,
            key="user-rating",
            score=score,
            comment=comment
        )