from fastapi import FastAPI, Request
from app.db import connect_to_db
from pydantic import BaseModel

app = FastAPI()

@app.on_event("startup")
async def startup():
    app.state.db = await connect_to_db()

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()


@app.get("/")
async def get_start():
    return "hello"