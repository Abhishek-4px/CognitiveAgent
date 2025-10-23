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


@app.middleware("http")
async def validation(request: Request , call_next):
    try:
        response = await call_next(request)
        return response 
    except Exception as e:
        logger.error("Validation error", error=str(e))
        return JSONResponse(status_code=400,content={"error":str(e)})




@app.get("/research/{task_id}")
async def check_status(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[task_id]

@app.post("/research/{task_id}/cancel")
async def cancel_task(task_id: str):
    if task_id not in tasks:
        raise HTTPException(status_code=404, detail="Task not found")
    tasks[task_id]["status"] = "cancelled"
    logger.info("Research cancelled", task_id=task_id)
    return {"task_id": task_id, "status": "cancelled"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}