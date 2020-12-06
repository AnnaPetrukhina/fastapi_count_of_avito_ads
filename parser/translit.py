import re

DICTIONARY = {
    'а': 'a',
    'б': 'b',
    'в': 'v',
    'г': 'g',
    'д': 'd',
    'е': 'e',
    'ё': 'e',
    'ж': 'zh',
    'з': 'z',
    'и': 'i',
    'й': 'i',
    'к': 'k',
    'л': 'l',
    'м': 'm',
    'н': 'n',
    'о': 'o',
    'п': 'p',
    'р': 'r',
    'с': 's',
    'т': 't',
    'у': 'u',
    'ф': 'f',
    'х': 'h',
    'ц': 'c',
    'ч': 'cz',
    'ш': 'sh',
    'щ': 'scz',
    'ъ': '',
    'ы': 'y',
    'ь': '',
    'э': 'e',
    'ю': 'u',
    'я': 'ya',
    ' ': '_',
    '-': '-'
}


def check_word(word):
    word = word.strip().lower()
    re_city = r"\b[а-яА-ЯёЁ]+[-\s]?[а-яА-ЯёЁ]*[-\s]?[а-яА-ЯёЁ]*\b"
    if re.fullmatch(re_city, word):
        return word
    else:
        return "россия"


def transliteration(word):
    word = check_word(word)
    translit_word = ""
    for symbol in word:
        translit_word += DICTIONARY[symbol]
    return translit_word
