from scholarly import scholarly
from include.scraper_api_proxy import ScraperAPI

# pg = ScraperAPI()
# pg.scraper_api(token="4e871db8cf293baa50ab751d2f073198")
# pg.FreeProxies()
# scholarly.use_proxy()

search_query = scholarly.search_pubs('"digital twin" AND "biotechnology"')
search_item = next(search_query)
node_id = hash(search_item['bib']['title'])

related = scholarly.get_related_articles(search_item)
related_item = next(related)

cited_by = scholarly.citedby(search_item)
cited_by_item = next(cited_by)

# author_query = scholarly.search_author(search_item['author_id'][-1])
# author_query_item = next(author_query)
# scholarly.pprint(author_query_item)

scholarly.pprint(search_item)
scholarly.pprint(cited_by_item)
scholarly.pprint(related_item)