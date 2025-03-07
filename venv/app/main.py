from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from .routers import users, tasks
from database.db import create_all_tables

app = FastAPI(lifespan=create_all_tables)
app.title = "Api de agenda"
app.version = "1.0"

app.include_router(users.router)
app.include_router(tasks.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials=True,
    allow_methods = ["*"],
    allow_headers=["*"]
)