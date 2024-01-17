import random
from .proxies import proxy_list

COUNT = 1

def construct_search_url(base_url, search_query, ordre_croissant=False, eligible_livraison_gratuite=False, quatre_etoile=False):
    url = base_url + search_query.replace(" ", "+")
    if ordre_croissant: 
        url += '&s=price-asc-rank'
    if eligible_livraison_gratuite:
        url += '&rh=p_n_free_shipping_eligible%3A20934939031'
    if quatre_etoile:
        url += '&rh=p_n_free_shipping_eligible%3A20934939031'
    return url

def set_increment():
    global COUNT
    COUNT = COUNT+1
def get_increment():
    return COUNT

def random_proxy():
    return random.choice(proxy_list)