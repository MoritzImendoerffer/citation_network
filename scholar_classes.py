from scholarly import scholarly
from include.scraper_api_proxy import ScraperAPI as ProxyGenerator
# from scholarly import ProxyGenerator
# import logging
# logging.basicConfig(level=logging.DEBUG)

class MyScholarlyScraper:
    def __init__(self, search_term: str):
        self.search_term = search_term
        self.search_result = None
        self.active_items = []
        self.cited_by = []
        self.citations = []
        self.related = []

    def search(self):
        res = scholarly.search_pubs(self.search_term)
        self.search_result = res

    def load_n_items(self, n=10, fill=False, citations=True, related=True):
        print(100 * '=')
        print('Started Load')
        print(100 * '=')
        if not self.search_result:
            try:
                self.search()
                print(100*'-')
                print(f'load_n_items: load SUCCESS')
                print(100 * '-')
            except Exception as e:
                print(100 * '-')
                print(f'load_n_items: load FAILED: {e}')
                print(100 * '-')

        for i in range(n):
            item = next(self.search_result)
            if fill:
                try:
                    item = scholarly.fill(item)
                    print(100 * '-')
                    print(f'load_n_items: fill SUCCESS')
                    print(100 * '-')
                except Exception as e:
                    print(100 * '-')
                    print(f'load_n_items: fill FAILED: {e}')
                    print(100 * '-')
            self.active_items.append(item)

            if citations:
                try:
                    cited_parser = scholarly.citedby(item)
                    self.cited_by.append(list(cited_parser))
                    print(100 * '-')
                    print(f'load_n_items: citations SUCCESS')
                    print(100 * '-')
                except Exception as e:
                    print(100 * '-')
                    print(f'load_n_items: citations FAILED: {e}')
                    print(100 * '-')
                    self.cited_by.append(None)

            if related:
                try:
                    related_parser = scholarly.get_related_articles(item)
                    self.related.append(list(related_parser))
                    print(100 * '-')
                    print(f'load_n_items: related SUCCESS')
                    print(100 * '-')
                except Exception as e:
                    print(100 * '-')
                    print(f'load_n_items: related FAILED: {e}')
                    print(100 * '-')
                    self.related.append(None)
        print(100*'=')
        print('Stopped Load')
        print(100 * '=')
    def citations(self):
        print('Not known yet, how to do that')