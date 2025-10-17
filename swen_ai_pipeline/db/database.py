"""
Database connection and session management.
"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine
)
from sqlalchemy.pool import NullPool
from swen_ai_pipeline.core.config import settings
from swen_ai_pipeline.db.models import Base


class Database:
    """
    Database connection manager.
    
    Handles the creation and management of database connections,
    sessions, and provides utilities for database operations.
    """
    
    def __init__(self):
        """Initialize the database manager."""
        self.engine: AsyncEngine | None = None
        self.async_session_maker: async_sessionmaker[AsyncSession] | None = None
    
    def init(self, database_url: str | None = None):
        """
        Initialize database engine and session maker.
        
        Args:
            database_url: Database connection URL. If None, uses settings.database_url
        """
        url = database_url or settings.database_url
        
        if not url:
            raise ValueError("Database URL is required")
        
        # Create async engine with connection pooling
        self.engine = create_async_engine(
            url,
            echo=settings.environment == "development",
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_timeout=settings.db_pool_timeout,
            pool_recycle=settings.db_pool_recycle,
            pool_pre_ping=True,
        )
        
        # Create session maker
        self.async_session_maker = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
            autocommit=False,
            autoflush=False
        )
    
    async def create_tables(self):
        """Create all database tables."""
        if not self.engine:
            raise RuntimeError("Database not initialized. Call init() first.")
        
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    
    async def drop_tables(self):
        """Drop all database tables. Use with caution!"""
        if not self.engine:
            raise RuntimeError("Database not initialized. Call init() first.")
        
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    
    async def close(self):
        """Close database connections."""
        if self.engine:
            await self.engine.dispose()
            self.engine = None
            self.async_session_maker = None
    
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Get a database session.
        
        Yields:
            AsyncSession: Database session
            
        Example:
            async with database.get_session() as session:
                result = await session.execute(query)
        """
        if not self.async_session_maker:
            raise RuntimeError("Database not initialized. Call init() first.")
        
        async with self.async_session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


# Global database instance
database = Database()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for FastAPI to get database session.
    
    Yields:
        AsyncSession: Database session
        
    Example:
        @app.get("/news")
        async def get_news(db: AsyncSession = Depends(get_db)):
            result = await db.execute(query)
    """
    async for session in database.get_session():
        yield session

