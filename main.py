import uvicorn
import db_manager
from fastapi import FastAPI, HTTPException
from schema import Params as SchemaParams
from schema import Counter as SchemaCounter
from parser import avito_parser
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
    check = await db_manager.check_params(params_search)
    if check:
        return {"search_id": check["id"]}
    else:
        id_search = await db_manager.create_params(params_search)
        return {"search_id": id_search}


@app.post("/check")
async def check_params(params_search: SchemaParams):
    check = await db_manager.check_params(params_search)
    return {"check": check}


@app.get("/{id}", response_model=SchemaParams)
async def get_params(id_search: int):
    params_search = await db_manager.get_params(id_search)
    if not params_search:
        raise HTTPException(status_code=404, detail="id not found")
    return SchemaParams(**params_search).dict()


@app.post("/parse", response_model=SchemaCounter)
def get_count_ads(params_search: SchemaParams):
    parser = avito_parser.AvitoParser(search_region=params_search.region, search=params_search.query)
    count = parser.parse_all()
    return SchemaCounter(**count).dict()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
