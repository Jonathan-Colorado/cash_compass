from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient

import uvicorn

from routers.accounts import router as accounts_router
from routers.users import router as users_router

DB_URL = config("DB_URL", cast=str)
DB_NAME = config("DB_NAME", cast=str)

# define origins
origins = ["*"]

# instantiate the app
app = FastAPI()

# add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    """connect to mongoDB at the start"""
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    """shut down database when app shuts down"""
    app.mongodb_client.close()

app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
app.include_router(users_router, prefix="/users", tags=["users"])
