from fastapi import FastAPI, HTTPException, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.core.logger import logger
from app.config import settings
from app.core.database import SessionLocal, ResearchTask, init_db
from app.core.redis_client import redis

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # replace with frontend url 
    allow_methods=["*"],
    allow_headers=["*"],
)



class ResearchRequest(BaseModel):
    query: str


