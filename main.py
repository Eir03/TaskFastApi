from fastapi import FastAPI
from api.endpoints import tasks

app = FastAPI(
    title="Апишка",
    description="Апи",
    version="1.0.0"
)

app.include_router(tasks.router)
