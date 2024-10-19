from fastapi import FastAPI
from celery_worker import celery_app

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/task")
async def create_task():
    task = celery_app.send_task('tasks.long_running_task')
    return {"task_id": task.id}

@app.get("/task/{task_id}")
async def get_task(task_id: str):
    task_result = celery_app.AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return result