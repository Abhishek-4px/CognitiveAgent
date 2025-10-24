from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.core.logger import logger
from app.config import settings
from app.core.database import SessionLocal, ResearchTask, init_db
from app.core.redis_client import redis,aioredis
from sqlalchemy.future import select
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # replace with frontend url 
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    await init_db()

class ResearchRequest(BaseModel):      #data validation
    query: str
    user_id: int


@app.middleware("http")
async def validation_middleware(request: ResearchRequest , call_next):
    try:
        response = await call_next(request)
        return response 
    except Exception as e:
        logger.error("Validation error", error=str(e))
        return JSONResponse(status_code=400,content={"error":str(e)})


@app.post("/research")
async def start_research(request: ResearchRequest):
    async with SessionLocal() as session:
        task=ResearchTask(
            status="started",
            query = request.query,
            user_id = request.user_id,
            created_at = datetime.utcnow()
        )
        session.add(task)
        await session.commit()
        await session.refresh(task)
        task_id = task.id
    await redis.lpush("research_queue", str(task_id))
    logger.info("Research started", task_id=task_id, query=request.query)
    return {"task_id": task_id}


@app.get("/research/{task_id}")
async def check_status(task_id:int):
    async with SessionLocal() as session:
        task = await session.get(ResearchTask, task_id)
        if not task:
            raise HTTPException(status_code=404 , detail="task not found")
        return {
            "task_id": task.id,
            "status": task.status,
            "query": task.qurey,
            "result": task.result,
            "error" : task.error,
            "created_at": task.created_at,
            "updated_at": task.updated_at,
            "user_id": task.user_id
        }
    

@app.post("/research/{task_id}/cancel")
async def cancel_request(task_id: int):
    await redis.set(f"cancel:{task_id}", 1)   # 1 tells rddis to concel the taskl
    async with SessionLocal() as session:
        task = await session.get(ResearchTask , task_id)
        if not task:
            raise HTTPException(status_code=404, detail="task not found")
        task.status= "cancelled"
        task.updated_at = datetime.utcnow()
        await session.commit()
    logger.info("Research cencelled", task_id = task_id)
    return {"task_id":task_id,"status":"cancelled"}


@app.get("/health")
async def health_check():
    return {"status":"ok"}
