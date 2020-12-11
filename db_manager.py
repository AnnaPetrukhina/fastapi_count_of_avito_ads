from fastapi import HTTPException

from models import db, search_params, counter
from schema import Params as SchemaParams
from parser import avito_parser


async def get_params(id_search: int):
    query = search_params.select().where(search_params.c.id == id_search)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return dict(result)


async def create_params(params: SchemaParams):
    check_search = search_params.select().where(search_params.c.region == params.region).where(
        search_params.c.query == params.query)
    result = await db.fetch_one(check_search)
    if result:
        return dict(result)
    else:
        query = search_params.insert().values(**params.dict())
        result = await db.execute(query)
        return {"id": result}


async def add_counter(params: dict):
    query = counter.insert().values(params)
    return await db.execute(query)


async def get_counter(id_search: int, start: str, end: str):
    query = counter.select().where(counter.c.id_search == id_search).where(counter.c.timestamp >= start).where(
        counter.c.timestamp <= end)
    post_list = await db.fetch_all(query)
    return [dict(result) for result in post_list]


async def parser(id_search: int):
    params = await get_params(id_search)
    try:
        pars = avito_parser.AvitoParser(search_region=params["region"], search=params["query"])
        counters = pars.parse_all()
        counters["id_search"] = id_search
        await add_counter(counters)
        return counters
    except Exception as exp:
        raise HTTPException(status_code=404, detail=f"{exp}")
