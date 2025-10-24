from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession , async_sessionmaker
from sqlalchemy.orm import declarative_base                   #orm : object relational mapper automated , to avoid sql injections
from sqlalchemy import Column, Text, String , Integer , DateTime
from datetime import datetime
from app.config import settings


engine = create_async_engine(settings.DATABASE_URL , echo =False)                      #connection to db
SessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False) #false ensures we dont have to hit the db again for query it saves in memry and remembers it
Base = declarative_base()

class ResearchTask(Base):
    __tablename__="research_tasks"
    id = Column(Integer, primary_key=True, index = True , autoincrement=True)
    status = Column(String, default="started")
    query = Column(Text)
    result = Column(Text , nullable = True)
    error = Column(Text , nullable = True)
    created_at = Column(DateTime , default=datetime.utcnow)
    updated_at = Column(DateTime , onupdate=datetime.utcnow)
    user_id = Column(Integer)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)      #converts the create_all sync to async

