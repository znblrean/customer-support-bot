import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from app.agents.support_agent import SupportAgent
from app.services.database import DatabaseService

@pytest.fixture
def mock_db_service():
    db = DatabaseService()
    db.redis = MagicMock()
    db.async_session = AsyncMock()
    return db

@pytest.mark.asyncio
async def test_process_message(mock_db_service):
    with patch('openai.ChatCompletion.create') as mock_openai:
        mock_openai.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="پاسخ تستی"))]
        )
        
        agent = SupportAgent(mock_db_service)
        response = await agent.process_message("سلام", "user123")
        
        assert "پاسخ تستی" in response["message"]
        assert len(response["session_id"]) == 36  # طول UUID

@pytest.mark.asyncio
async def test_sentiment_detection(mock_db_service):
    agent = SupportAgent(mock_db_service)
    with patch('openai.ChatCompletion.create') as mock_openai:
        mock_openai.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="negative"))]
        )
        sentiment = agent._detect_sentiment("من خیلی ناراضی هستم")
        assert sentiment == "negative"