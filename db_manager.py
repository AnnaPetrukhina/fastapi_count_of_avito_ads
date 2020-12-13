from fastapi import HTTPException

from models import db, search_params, counter
from schema import Params as SchemaParams
from parser_avito import avito_parser


async def get_params(id_search: int) -> dict:
    """Получение поисковой фразы и региона по id из БД.

    :param id_search: id, которое соответствует поисковой фразе и региону
    :raises HTTPException: если id_search нет в БД
    :return result: поисковая фраза и региону, соответствующие id
    """
    query = search_params.select().where(search_params.c.id == id_search)
    result = await db.fetch_one(query)
    if not result:
        raise HTTPException(status_code=404, detail="id not found")
    return dict(result)


async def create_params(params: SchemaParams) -> dict:
    """Добавление поисковой фразы и региона в БД с присвоением им id.

    :param params: поисковая фраза и регион
    :return result: поисковая фраза с регионом и соответствующий им id
    """
    check_search = search_params.select().where(search_params.c.region == params.region).where(
        search_params.c.query == params.query)
    result = await db.fetch_one(check_search)
    if result:
        return dict(result)
    else:
        query = search_params.insert().values(**params.dict())
        result = await db.execute(query)
        return {"id": result, **params.dict()}


async def add_counter(params: dict) -> None:
    """Добавление id, счетчика и временной метки в БД.

    :param params: id региона с поисковой фразой, кол-во объявлений и временная метка
    :return None
    """
    query = counter.insert().values(params)
    await db.execute(query)


async def get_counter(id_search: int, start: str, end: str) -> list:
    """Получение из БД счетчика, временной метки и id за оперделенный период.

    :param id_search: id, которое соответствует поисковой фразе и региону
    :param start: начало периода
    :param end: конец периода
    :return result: id региона с поисковой фразой, кол-во объявлений и временная метка,
    которые находятся в данном периоде
    """
    query = counter.select().where(counter.c.id_search == id_search).where(counter.c.timestamp >= start).where(
        counter.c.timestamp <= end)
    post_list = await db.fetch_all(query)
    return [dict(result) for result in post_list]


async def parser(id_search: int) -> dict:
    """Получение счетчика, временной метки по id со страницы авито, соответствующей поисковой фразе и региону
    полученного id.

    :param id_search: id, которое соответствует поисковой фразе и региону
    :raises HTTPException: ошибки, которые могут возникнуть при парсиге страницы
    :return result: id, кол-во объявлений и временная метка соответствующего региона с поисковой фразой
    """
    params = await get_params(id_search)
    try:
        pars = avito_parser.AvitoParser(search_region=params["region"], search=params["query"])
        counters = pars.parse_all()
        counters["id_search"] = id_search
        await add_counter(counters)
        return counters
    except Exception as exp:
        raise HTTPException(status_code=404, detail=f"{exp}")
