from scholarly import scholarly
import concurrent.futures
from include.scraper_api_proxy import ScraperAPI as ProxyGenerator
# from scholarly import ProxyGenerator
# import logging
# logging.basicConfig(level=logging.DEBUG)

class MyScholarlyScraper:
    def __init__(self, search_term: str, n_threads=10):
        self.search_term = search_term
        self.search_result = None
        self.active_items = []
        self.cited_by = []
        self.citations = []
        self.related = []
        self.n_threads = n_threads

    def search(self):
        res = scholarly.search_pubs(self.search_term)
        self.search_result = res

    def load_n_items(self, n=10, fill=True, citations=True, related=True):
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

        # exhaust n items
        search_items = [next(self.search_result) for i in range(n)]

        # label the items to sort all results after threading using a consecutive index
        if self.active_items:
            start_index = min([item[0]] for item in self.active_items)[0]
        else:
            start_index = 0
        ind = subsequent_iterator(start_index, 1e8)

        # search items always should look like (index, item, ...)
        search_items = [(next(ind), item) for item in search_items]

        if fill:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.n_threads) as executor:
                search_items_filled = list(executor.map(lambda item: get_filled(item), search_items))

            self.active_items.extend(search_items_filled)
        else:
            self.active_items.extend(search_items)

        if citations:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.n_threads) as executor:
                cited_by = list(executor.map(lambda item: get_cited_by(item), search_items))
            self.cited_by.extend(cited_by)

        if related:
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.n_threads) as executor:
                related_list = list(executor.map(lambda item: get_related(item), search_items))
            self.related.extend(related_list)

        self.active_items.sort(key=lambda x: x[0])
        self.cited_by.sort(key=lambda x: x[0])
        self.related.sort(key=lambda x: x[0])

def subsequent_iterator(a=0, n=1e3):
    n = int(n)
    for i in range(a, a+n):
        yield i

def get_related(item):
    print(100 * '-')
    print(f'get_related: Started')
    print(100 * '-')
    success = False

    index, _item = item
    try:
        related_parser = scholarly.get_related_articles(_item)
        related_list = list(related_parser)
        success = True
    except Exception as e:
        print(f'get_related: Exception: {e}')
        related_list = None

    print(100 * '-')
    print(f'get_related: Stopped, Success = {success}')
    print(100 * '-')
    return (index, related_list, success)

def get_cited_by(item):
    print(100 * '-')
    print(f'get_citations: Started')
    print(100 * '-')
    success = False

    index, _item = item
    try:
        cited_parser = scholarly.citedby(_item)
        cited_list = list(cited_parser)
        success = True
    except Exception as e:
        print(f'get_cited_by: Exception: {e}')
        cited_list = None

    print(100 * '-')
    print(f'get_citations: Stopped, Success = {success}')
    print(100 * '-')
    return (index, cited_list, success)

def get_filled(item):
    print(100 * '-')
    print(f'fill: Started')
    print(100 * '-')
    success = False

    index, _item = item
    try:
        _item = scholarly.fill(_item)
        success = True
    except Exception as e:
        print(f'get_filled: Exception: {e}')
        pass

    print(100 * '-')
    print(f'fill: Stopped, Success = {success}')
    print(100 * '-')
    return (index, _item, success)