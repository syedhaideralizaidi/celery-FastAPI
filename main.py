from celery.result import AsyncResult
from fastapi import FastAPI
from pydantic import BaseModel
from celery import Celery

app = FastAPI()

celery = Celery(__name__, broker='redis://localhost:6379/0')
celery.conf.task_send_sent_event = True

@celery.task
def long_running_task(a, b):
    import time
    time.sleep(10)
    print("hello")
    return a + b

class TaskRequest(BaseModel):
    a: int
    b: int

@app.post("/run_task")
def run_task(request: TaskRequest):
    long_running_task.delay(request.a, request.b)
    return {"message": "Task started"}

@app.get("/task_status/{task_id}")
def get_task_status(task_id: str):
    task = AsyncResult(task_id)
    return {"status": task.status, "result": task.result}