pip install celery redis
from celery import Celery
app = FastAPI()
celery = Celery(__name__, broker='redis://localhost:6379/0')
@celery.task
def long_running_task(a, b):
    import time
    time.sleep(10)
    return a + b
# Define a FastAPI endpoint that triggers the Celery task
@app.post("/run_task")
def run_task(a: int, b: int):
    long_running_task.delay(a, b)
    return {"message": "Task started"}
Run celery worker first with this command:
celery -A main.celery worker --beat --loglevel=info
Then run fastAPI application and hit your desired endpoint:
 uvicorn main:app --reload
