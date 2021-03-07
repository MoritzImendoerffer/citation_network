from scholarly import ProxyGenerator
from urllib.parse import urlencode


class ScraperAPI(ProxyGenerator):
    def __init__(self):
        super().__init__()

    def scraper_api(self, token):
        self._TIMEOUT = 60
        base_url = 'http://api.scraperapi.com/?'
        payload = {'api_key': token}
        proxy_url = base_url + urlencode(payload)
        self._use_proxy(http=proxy_url)
