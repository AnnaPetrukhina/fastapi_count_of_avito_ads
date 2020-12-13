import json

import pytest
from httpx import AsyncClient

from main import app
import db_manager

test_data_add = [
    ({"region": "москва", "query": "книга"}, {"id": 1, "region": "москва", "query": "книга"}, [200, {"id": 1}]),
    ({"region": "клин", "query": "книга"}, {"id": 2, "region": "клин", "query": "книга"}, [200, {"id": 2}]),
    pytest.param({"query": "книга"}, {"id": 2, "query": "книга"},
                 [422, {"id": 2}], marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param({"region": "москва", "query": "книга"}, {"id": 1, "region": "москва", "query": "книга"},
                 [200, {"id": 2}], marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param({"region": "москва", "query": 1}, {"id": 1, "region": "москва", "query": 1},
                 [200, {"id": 2}], marks=pytest.mark.xfail(raises=AssertionError)),
    pytest.param({"region": "москва", "query": "книга"}, {"id": 1, "region": "москва", "query": "книга"},
                 [422, {"id": 1}], marks=pytest.mark.xfail(raises=AssertionError)),
    ({"region": "moskva", "query": "книга"}, {"id": 1, "region": "moskva", "query": "книга"},
     [422,
      {
          "detail": [
              {
                  "loc": [
                      "body",
                      "region"
                  ],
                  "msg": "string does not match regex \"\\b[а-яА-ЯёЁ]+[-\\s]?[а-яА-ЯёЁ]*[-\\s]?[а-яА-ЯёЁ]*\\b\"",
                  "type": "value_error.str.regex",
                  "ctx": {
                      "pattern": "\\b[а-яА-ЯёЁ]+[-\\s]?[а-яА-ЯёЁ]*[-\\s]?[а-яА-ЯёЁ]*\\b"
                  }
              }
          ]
      }]),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("request_params, create_params_mock, expected", test_data_add)
async def test_create_params(monkeypatch, request_params, create_params_mock, expected):
    async def mock_create_params(params):
        return create_params_mock

    monkeypatch.setattr(db_manager, "create_params", mock_create_params)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/add", data=json.dumps(request_params))

    assert response.status_code == expected[0]
    assert response.json() == expected[1]


data = (
    {"id_search": 1, "hours": 1},
    {"id_search": 1, "timestamp": "18:30:51 13.12.2020", "count": 331650},
    [{"id_search": 1, "timestamp": "18:30:51 13.12.2020", "count": 331650},
     {"id_search": 1, "timestamp": "19:30:51 13.12.2020", "count": 331650}],
    [200, [{"id_search": 1, "timestamp": "18:30:51 13.12.2020", "count": 331650},
     {"id_search": 1, "timestamp": "19:30:51 13.12.2020", "count": 331650}], 2])


test_data_stat = [data,
                  pytest.param(data[0], data[1], [data[1]], data[3], marks=pytest.mark.xfail(raises=AssertionError)),
                  pytest.param({"id_search": "один", "hours": 1}, data[1], data[2], data[3],
                               marks=pytest.mark.xfail(raises=AssertionError)),
                  ]


@pytest.mark.asyncio
@pytest.mark.parametrize("request_params, parser_mock, get_counter_mock, expected", test_data_stat)
async def test_get_count(monkeypatch, request_params, parser_mock, get_counter_mock, expected):
    async def mock_parser(id_search):
        return parser_mock

    async def mock_get_counter(id_search, start, end):
        return get_counter_mock

    monkeypatch.setattr(db_manager, "parser", mock_parser)
    monkeypatch.setattr(db_manager, "get_counter", mock_get_counter)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get(f"/stat?id_search={request_params['id_search']}&hours={request_params['hours']}")

    assert response.status_code == expected[0]
    assert response.json() == expected[1]
    assert len(response.json()) == expected[2]
