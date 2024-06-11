from contextlib import asynccontextmanager
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from models import teacher

@asynccontextmanager
async def connect_to_db(app: FastAPI):
    client = AsyncIOMotorClient("mongodb://localhost")

    await init_beanie(database=client["SMIC"], document_models=[
        teacher.Teachers
    ])
    print("yoyoyo we up in this jawn")

    yield
    client.close()
    print("yoyoyo we outta this jawn")
