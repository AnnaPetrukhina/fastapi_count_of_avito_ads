from models import db, search_params
from schema import Params as SchemaParams


async def get_params(id_search: int):
    query = search_params.select().where(search_params.c.id == id_search)
    return await db.fetch_one(query)


async def check_params(params: SchemaParams):
    check_search = search_params.select().where(search_params.c.region == params.region and
                                                search_params.c.query == params.query)
    return await db.fetch_one(check_search)


async def create_params(params: SchemaParams):
    query = search_params.insert().values(**params.dict())
    return await db.execute(query)
