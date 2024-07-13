import asyncio
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/longrun")
async def longrun():
    await asyncio.sleep(1)
    return {"message": "Slow response"}