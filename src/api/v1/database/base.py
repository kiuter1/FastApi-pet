import os

from dotenv import load_dotenv
from miniopy_async import Minio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

DATABASE_URL = f"mysql+asyncmy://{os.getenv('SQL_USER')}:{os.getenv('SQL_PASSWORD')}@{os.getenv('SQL_HOST')}/{os.getenv('SQL_DATABASE')}"

client = Minio(os.getenv('S3_ENDPOINT'),
        access_key=os.getenv('S3_ACCESS'),
        secret_key=os.getenv('S3_SECRET'),
        secure=os.getenv('S3_SECURE')
    )

engine = create_async_engine(DATABASE_URL)

AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()