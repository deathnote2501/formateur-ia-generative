from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os # For environment variables

# DATABASE_URL should be loaded from environment variables
# Example: "postgresql+asyncpg://user:password@host:port/dbname"
# For now, using a placeholder.
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@localhost/dbname_placeholder")

async_engine = create_async_engine(DATABASE_URL, echo=True) # echo=True for logging SQL, can be removed in production

AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
