import logging
from datetime import datetime
from typing import List
import asyncio

import uvicorn
from fastapi import FastAPI

import db_manager
from models import db
from schema import Params as SchemaParams, Counter as SchemaCounter, ParamsOut as SchemaParamsOut


log = logging.getLogger('fastapi_avito')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("fastapi_avito.log", 'w', 'utf-8', delay=True)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M %d-%m-%Y')
fh.setFormatter(formatter)
log.addHandler(fh)


app = FastAPI(title="Async FastAPI")


@app.on_event("startup")
async def startup() -> None:
    """Полключение к БД при запуске."""
    log.debug("Подключение к БД")
    await db.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    """Отключение от БД при выключении."""
    log.debug("Отключение от БД")
    await db.disconnect()


@app.post("/add", response_model=SchemaParamsOut)
async def create_params(params_search: SchemaParams) -> dict:
    """Получение id поисковой фразы и региона.

    :param params_search: поисковая фраза и регион
    :return id_search: id, которое было присвоено поисковой фразе и региону
    """
    id_search = await db_manager.create_params(params_search)
    log.debug(f"Метод add {id_search}")
    return id_search


@app.get("/stat", response_model=List[SchemaCounter])
async def get_count(id_search: int, hours: int) -> list:
    """Получение временной метки и количества объявлений по id поисковой фразы и соответствующеего региона.

    :param id_search: id, которое соответствует поисковой фразе и региону
    :param hours: период (кол-во часов), за который надо вывести счетчики
    :return counter: список всех счетчиков и временных меток за данный период
    """
    log.debug(f"Метод stat для id:{id_search} c периодом:{hours}")
    start = datetime.now().strftime("%H:%M %d.%m.%Y")
    while hours >= 0:
        await db_manager.parser(id_search)
        await asyncio.sleep(60 * 60)
        hours -= 1
    end = datetime.now().strftime("%H:%M %d.%m.%Y")
    counter = await db_manager.get_counter(id_search, start, end)
    log.debug(f"Получено {counter}")
    return counter


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
