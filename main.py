import uvicorn
from fastapi import FastAPI, HTTPException
from schema import Params as SchemaParams
import db_manager
from models import db


app = FastAPI(title="Async FastAPI")


@app.on_event("startup")
async def startup():
    await db.connect()


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()


@app.post("/add")
async def create_params(params_search: SchemaParams):
    check = await db_manager.check(params_search)
    if check:
        return {"search_id": check["id"]}
    else:
        id_search = await db_manager.create(params_search)
        return {"search_id": id_search}


@app.post("/check")
async def check_params(params_search: SchemaParams):
    check = await db_manager.check(params_search)
    return {"check": check}


@app.get("/{id}", response_model=SchemaParams)
async def get_params(id_search: int):
    params_search = await db_manager.get(id_search)
    if not params_search:
        raise HTTPException(status_code=404, detail="id not found")
    return SchemaParams(**params_search).dict()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
