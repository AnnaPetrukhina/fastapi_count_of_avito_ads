import pytest

from parser_avito import translit

test_data_transliteration = [("москва", "moskva"),
                             ("россия", "rossiya"),
                             ("1", "rossiya"),
                             ("Санкт-Петербург", "sankt-peterburg"),
                             ("Йошкар-Ола", "yoshkar-ola"),
                             pytest.param("Щелково", "SHCHelkovo", marks=pytest.mark.xfail(raises=AssertionError)),
                             pytest.param("Шелехово", "SHelekhovo", marks=pytest.mark.xfail(raises=AssertionError)),
                             ]

test_data_check = [("москва", "москва"),
                   ("россия", "россия"),
                   ("1", "россия"),
                   ("Санкт-Петербург", "санкт-петербург"),
                   ("Йошкар-Ола", "йошкар-ола"),
                   ("КЛИН", "клин"),
                   ("мОСКВА", "москва"),
                   ("мОСКВА1", "россия")
                   ]


@pytest.mark.parametrize("params, expected", test_data_transliteration)
def test_transliteration(params, expected):
    assert translit.transliteration(params) == expected


@pytest.mark.parametrize("params, expected", test_data_check)
def test_check_word(params, expected):
    assert translit.check_word(params) == expected
