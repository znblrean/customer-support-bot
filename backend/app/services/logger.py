from langsmith.schemas import Run, Example
from app.utils.tracing import setup_tracing

client = setup_tracing()

def log_conversation(user_input: str, bot_response: str, session_id: str):
    client.create_feedback(
        run_id=session_id,
        key="user-rating",
        score=1,  # می‌توانید از کاربر دریافت کنید
        comment=""
    )
    
    client.log_example(
        inputs={"input": user_input},
        outputs={"output": bot_response},
        dataset_id="customer-support-dataset"
    )