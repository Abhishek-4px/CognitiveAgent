from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession , async_sessionmaker
from sqlalchemy.orm import declarative_base , Mapped , mapped_column                #orm : object relational mapper automated , to avoid sql injections
from sqlalchemy import Column, Text, String , Integer , DateTime
from datetime import datetime
from app.config import settings
from typing import Optional

engine = create_async_engine(settings.DATABASE_URL , echo =False)                      #connection to db
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False) #false ensures we dont have to hit the db again for query it saves in memry and remembers it
Base = declarative_base()

class ResearchTask(Base):
    __tablename__ = "research_tasks"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String, default="started")
    query: Mapped[str] = mapped_column(Text)
    result: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    error: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, onupdate=datetime.utcnow)
    user_id: Mapped[int] = mapped_column(Integer)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)      #converts the create_all sync to async

