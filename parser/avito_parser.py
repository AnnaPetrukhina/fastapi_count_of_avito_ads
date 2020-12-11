import logging
from datetime import datetime
from typing import Optional

from selenium.webdriver import Chrome, ChromeOptions
import bs4

from parser.translit import transliteration


log = logging.getLogger('parser_avito')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("parser_avito.log", 'w', 'utf-8', delay=True)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M %d-%m-%Y')
fh.setFormatter(formatter)
log.addHandler(fh)


class AvitoParser:
    """Класс AvitoParser используется для получения количества объявлений по поисковой фразе и в определенном регионе.

    Attributes
    ----------
    search: поисковая фраза
    search_region: регион поиска

    Methods
    -------
    _get_page(page: int = None):
        Получение информации со страницы.
    check_page(text: bs4.BeautifulSoup):
        Проверка сущуствует ли данная страница.
    get_number_of_ads(page: int = None):
        Получение количества объявлений на странице.
    parse_all():
        Получения количества страниц и временной метки.
    """

    def __init__(self, search: str, search_region: str) -> None:
        """Устанавливает все необходимые атрибуты для объекта класса AvitoParser.

        :param search: поисковая фраза
        :param search_region: регион поиска
        """
        options = ChromeOptions()
        options.add_argument('no-sandbox')
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        self.browser = Chrome(options=options)
        self.search = search.strip().replace(" ", "+")
        self.region = transliteration(search_region)

    def _get_page(self, page: Optional[int] = None) -> bs4.BeautifulSoup:
        """Получение информации со страницы.

        :param page: страница поиска (по умолчанию None)
        :return soup: весь html-код страницы
        """
        url = f"https://www.avito.ru/{self.region}?q={self.search}&s=104"
        if page and page > 1:
            url = f"https://www.avito.ru/{self.region}?p={page}&q={self.search}&s=104"
        log.debug(f"url:{url}")
        self.browser.get(url)
        text = self.browser.page_source
        soup = bs4.BeautifulSoup(text, 'lxml')
        return soup

    @staticmethod
    def check_page(text: bs4.BeautifulSoup) -> bool:
        """Проверка существует ли данная старница.

        :param text: html-код страницы
        :raises ValueError: если страницы нет
        :return True
        """
        wrong = text.find('div', class_='b-404')
        if wrong:
            log.exception(f"{wrong.contents[1].contents[0]}")
            raise ValueError("Такой страницы нет")
        return True

    def get_number_of_ads(self,  page: Optional[int] = None) -> str:
        """Получение количества объявлений.

        :param page: страница поиска (по умолчанию None)
        :return count: количество объявлений на существующей страницы и нуля, если страницы нет строкой
        """
        text = self._get_page(page)
        if self.check_page(text):
            container = text.select('span.page-title-count-1oJOc')[0].contents
            return container[0]
        else:
            return "0"

    def parse_all(self) -> dict:
        """Получение количества объявлений и временной метки.

        :return result: число объявлений и временная метка
        """
        now = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
        log.debug(f"время: {now}")
        count_ads = self.get_number_of_ads()
        count_ads = int(count_ads.replace(" ", ""))
        log.debug(f"количество объявлений: {count_ads}")
        self.browser.close()
        return {"count": count_ads, "timestamp": now}


if __name__ == '__main__':
    search_query = "книга"
    region = "Москва"
    parser_avito = AvitoParser(search_query, region)
    data = parser_avito.parse_all()
    print(data)
