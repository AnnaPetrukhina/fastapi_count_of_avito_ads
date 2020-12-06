import logging
from selenium.webdriver import Chrome, ChromeOptions
from datetime import datetime
from parser.translit import transliteration
import bs4

log = logging.getLogger('parser_avito')
log.setLevel(logging.DEBUG)
fh = logging.FileHandler("parser_avito.log", 'w', 'utf-8', delay=True)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M')
fh.setFormatter(formatter)
log.addHandler(fh)


class AvitoParser:

    def __init__(self, search, search_region):
        options = ChromeOptions()
        options.add_argument('no-sandbox')
        options.add_argument('headless')
        options.add_argument('disable-gpu')
        self.browser = Chrome(options=options)
        self.count_page = 0
        self.search = search.strip().replace(" ", "+")
        self.region = transliteration(search_region)

    def _get_page(self, page: int = None):
        url = f"https://www.avito.ru/{self.region}?q={self.search}&s=104"
        if page and page > 1:
            url = f"https://www.avito.ru/{self.region}?p={page}&q={self.search}&s=104"
        log.debug(f"url:{url}")
        self.browser.get(url)
        text = self.browser.page_source
        soup = bs4.BeautifulSoup(text, 'lxml')
        return soup

    @staticmethod
    def check_page(text: bs4.BeautifulSoup):
        wrong = text.find('div', class_='b-404')
        if wrong:
            log.info(f"{wrong.contents[1].contents[0]}")
            return False
        return True

    def get_number_of_ads(self,  page: int = None):
        text = self._get_page(page)
        if self.check_page(text):
            container = text.select('span.page-title-count-1oJOc')[0].contents
            return container[0]
        else:
            return "0"

    def parse_all(self):
        now = datetime.now().strftime("%H:%M:%S %d.%m.%Y")
        log.debug(f"время: {now}")
        self.count_page = self.get_number_of_ads()
        self.count_page = int(self.count_page.replace(" ", ""))
        log.debug(f"количество объявлений: {self.count_page}")
        self.browser.close()
        return {"count": self.count_page, "timestamp": now}


if __name__ == '__main__':
    # search_query = "беговая дорожка"
    search_query = "книга"
    # "россия", "московская облость" "московская область" "Санкт-Петербург" "Москва"
    region = "Москва"
    parser_avito = AvitoParser(search_query, region)
    data = parser_avito.parse_all()
    print(data)
