from fastapi import FastAPI, HTTPException , Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse 
from pydantic import BaseModel
import uuid    #unique ids for research tasks
from app.core.logger import logger
from app.config import settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # replace with frontend url 
    allow_methods=["*"],
    allow_headers=["*"],
)

tasks= {}    # empty now to be replaced with Database later

class ResearchRequest(BaseModel):
    query: str

