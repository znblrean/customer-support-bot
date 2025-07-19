<<<<<<< HEAD
from app.utils.logger import logger  # باید با نام موجود در logger.py مطابقت داشته باشد
=======
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

class DatabaseService:
    def __init__(self):
        self.engine = None
        self.async_session = None

    async def initialize(self):
        db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/dbname")
        self.engine = create_async_engine(db_url)
        self.async_session = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.conversation import Base
from app.utils.logger import logger
import redis

class DatabaseService:
    def __init__(self):
        self.redis = None
        self.async_engine = None
        self.async_session = None

    async def initialize(self):
        """راه‌اندازی اتصالات به دیتابیس"""
        try:
            # PostgreSQL (Async)
            db_url = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/dbname")
            self.async_engine = create_async_engine(db_url, echo=False)
            self.async_session = sessionmaker(
                self.async_engine, expire_on_commit=False, class_=AsyncSession
            )
            
            # Redis برای حافظه کوتاه‌مدت
            self.redis = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=int(os.getenv("REDIS_DB", 0)),
                decode_responses=True
            )
            
            # ایجاد جداول (در حالت توسعه)
            if os.getenv("ENV") == "development":
                async with self.async_engine.begin() as conn:
                    await conn.run_sync(Base.metadata.create_all)
            
            logger.info("Database connections established successfully")
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            raise

    async def get_session(self):
        """تهیه یک session جدید برای کار با دیتابیس"""
        if not self.async_session:
            raise RuntimeError("Database not initialized")
        return self.async_session()

    async def store_conversation(self, conversation_data):
        """ذخیره مکالمه در دیتابیس"""
        async with await self.get_session() as session:
            try:
                new_conversation = Conversation(**conversation_data)
                session.add(new_conversation)
                await session.commit()
                return new_conversation
            except Exception as e:
                await session.rollback()
                logger.error(f"Error storing conversation: {str(e)}")
                raise
>>>>>>> cfb62a60 (new pip install langsmith langchain openai)
