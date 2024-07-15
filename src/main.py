import asyncio
from typing import Any, Dict

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root() -> Dict[str, Any]:
    return {"message": "Hello World"}


@app.get("/longrun")
async def longrun() -> Dict[str, Any]:
    await asyncio.sleep(1)
    return {"message": "Slow response"}
