import asyncio
from datetime import datetime
from typing import List

import db_manager
import uvicorn
from fastapi import FastAPI

from models import db
from schema import Params as SchemaParams, Counter as SchemaCounter, ParamsOut as SchemaParamsOut


app = FastAPI(title="Async FastAPI")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.post("/add", response_model=SchemaParamsOut)
async def create_params(params_search: SchemaParams):
    id_search = await db_manager.create_params(params_search)
    return id_search


@app.get("/stat", response_model=List[SchemaCounter])
async def get_count(id_search: int, hours: int):
    start = datetime.now().strftime("%H:%M %d.%m.%Y")
    while hours > 0:
        await db_manager.parser(id_search)
        await asyncio.sleep(60 * 60)
        hours -= 1
    end = datetime.now().strftime("%H:%M %d.%m.%Y")
    counter = await db_manager.get_counter(id_search, start, end)
    return counter


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
