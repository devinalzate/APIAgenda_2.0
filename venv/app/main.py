from fastapi import FastAPI
from .routers import users, tasks
from database.db import create_all_tables

app = FastAPI(lifespan=create_all_tables)
app.title = "Api de agenda"
app.version = "1.0"

app.include_router(users.router)
app.include_router(tasks.router)