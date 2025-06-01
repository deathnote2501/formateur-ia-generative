from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker # For async_sessionmaker

# Placeholder for the database URL, should be loaded from environment variables in a real app
DATABASE_URL = "postgresql+asyncpg://user:password@host:port/dbname_dev"

async_engine = create_async_engine(DATABASE_URL, echo=True) # Added echo=True for debugging, can be removed later

# For SQLAlchemy 2.0, async_sessionmaker is preferred
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession, # Use AsyncSession for the session class
    autocommit=False,
    autoflush=False,
    expire_on_commit=False # Good practice for async sessions
)

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit() # Commit if all operations within the session were successful
        except Exception:
            await session.rollback() # Rollback on error
            raise
        finally:
            await session.close() # Ensure session is closed
