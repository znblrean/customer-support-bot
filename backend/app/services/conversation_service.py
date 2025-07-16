from langchain.schema import HumanMessage, AIMessage
from langchain.callbacks.manager import CallbackManager
from app.utils.langsmith_config import langsmith_tracer

class ConversationService:
    def __init__(self):
        self.callback_manager = CallbackManager([langsmith_tracer])
        
    async def log_conversation(self, user_input: str, bot_response: str):
        messages = [
            HumanMessage(content=user_input),
            AIMessage(content=bot_response)
        ]
        
        # Log to LangSmith
        self.callback_manager.on_chain_end(
            {"messages": messages},
            metadata={"conversation": True}
        )