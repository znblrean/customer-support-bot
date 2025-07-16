import pytest
from sqlalchemy.ext.asyncio import create_async_engine
from app.services.database import DatabaseService
from app.models.conversation import Conversation

@pytest.mark.asyncio
async def test_database_operations():
    # استفاده از دیتابیس تست در حافظه
    db_service = DatabaseService()
    db_service.async_engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    await db_service.initialize()
    
    async with await db_service.get_session() as session:
        # تست ذخیره و بازیابی
        test_data = {
            "user_id": "test_user",
            "session_id": "test_session",
            "user_message": "سلام",
            "bot_response": "سلام! چطور می‌توانم کمک کنم؟",
            "sentiment": "positive",
            "intent": "greeting"
        }
        
        # ذخیره
        await db_service.store_conversation(test_data)
        
        # بازیابی
        result = await session.execute(select(Conversation))
        conversations = result.scalars().all()
        
        assert len(conversations) == 1
        assert conversations[0].user_id == "test_user"