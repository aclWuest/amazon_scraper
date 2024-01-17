import asyncio
import json
from bs4 import BeautifulSoup
from .config import LIMIT, HEADERS
from .utils import  set_increment, get_increment, random_proxy
from .product import Product

async def fetch_page(session, url,referer=None):
    """
    Asynchrone. Récupère le contenu d'une page web.
    
    Envoie une requête GET asynchrone à l'URL spécifiée en utilisant la session donnée 
    et renvoie le contenu de la page si la requête est réussie.
    
    Args:
        session (aiohttp.ClientSession): La session HTTP à utiliser pour la requête.
        url (str): L'URL de la page à récupérer.
        HEADERS: Headers récupérés depuis httpbin
    Retourne:
        Le contenu HTML de la page sous forme de string, ou lève une Exception en cas d'échec.
    """
    if referer: 
        HEADERS['Referer'] = referer
    async with session.get(url, headers=HEADERS) as response:
        if response.status == 200:
            return await response.text()
        else:
            raise ConnectionRefusedError(response)

async def extract_product_links(html_content):
    """
    Asynchrone. Extrait les liens des produits à partir du contenu HTML.
    
    Analyse le contenu HTML de la page de recherche pour trouver les numéros 
    d'identification (ASIN) des produits individuels et filtre les produits 
    sponsorisés
    
    Args:
        html_content (str): Le contenu HTML de la page de recherche.
    
    Retourne:
        Une liste des liens (ASINs) des produits non sponsorisés.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    return [a.get('data-asin') for a in soup.find_all('div', attrs={'data-component-type': 's-search-result'}) 
            if not a.find('span', attrs={'class': 'puis-label-popover-default'}) ]


async def fetch_and_extract_product_data(session, product_url, base_url):
    """
    Asynchrone. Récupère et extrait les données d'un produit.
    
    Combine les fonctions fetch_page et extract_product_data pour récupérer 
    les détails d'un produit à partir de son URL et extraire les données pertinentes.
    
    Args:
        session (aiohttp.ClientSession): La session HTTP à utiliser pour la requête.
        product_url (str): L'URL de la page produit.
        base_url: L'URL de la recherche.
    
    Retourne:
        Un dictionnaire contenant les données extraites du produit.
    """
    product_page_content = await fetch_page(session, product_url, base_url)
    if product_page_content:
        return await Product(product_page_content).extract_info()
    return None

async def scrape_product_details(session, product_links, base_url):
    """
    Asynchrone. Traite les détails de plusieurs produits.
    
    Crée des tâches asynchrones pour récupérer et extraire les données 
    de chaque produit listé dans product_links.
    
    Args:
        session (aiohttp.ClientSession): La session HTTP à utiliser pour les requêtes.
        product_links (list): Une liste des liens (ASINs) des produits à scraper.
    Yields:
        Les données extraites de chaque produit sous forme de dictionnaire.
    """
    tasks = [asyncio.create_task(fetch_and_extract_product_data(session, f"https://www.amazon.fr/dp/{asin}", base_url)) for asin in product_links]
    for task in asyncio.as_completed(tasks):
        product_data = await task
        if product_data:
            yield product_data

async def write_product_data(session, product_links, json_file, base_url):
    """
    Asynchrone. Écrit les données des produits dans un fichier JSON.

    Utilise `scrape_product_details` pour obtenir les données des produits 
    et les écrit de manière asynchrone dans le fichier JSON spécifié.

    Args:
        session (aiohttp.ClientSession): La session HTTP à utiliser.
        product_links (list): Les liens (ASINs) des produits à écrire.
        json_file (aiofiles file): Le fichier JSON où écrire les données.
    """
    async for product_data in scrape_product_details(session, product_links, base_url):
        await json_file.write(json.dumps(product_data, indent=2,ensure_ascii=False) + ',\n')
        if get_increment() >= LIMIT:
            break 
        set_increment()

async def find_total_pages(session, initial_page_url):
    """
    Asynchrone. Détermine le nombre total de pages de résultats.

    Analyse la première page de résultats de recherche pour trouver le nombre 
    total de pages disponibles, en se basant sur la pagination affichée.

    Args:
        session (aiohttp.ClientSession): La session HTTP à utiliser pour la requête.
        initial_page_url (str): L'URL de la première page de résultats de recherche.

    Retourne:
        Le nombre total de pages de résultats sous forme d'entier.
    """
    html_content = await fetch_page(session, initial_page_url)
    if html_content:
        soup = BeautifulSoup(html_content, 'lxml')
        pagination = soup.find_all(
            'span', attrs={'class': ['s-pagination-item', 's-pagination-disabled']})
        return int(pagination[-1].text)
    return 1

async def scrape_product_page_generator(session, url, json_file):
    """
    Asynchrone. Générateur qui scrape une page de produits et écrit les données.

    Récupère le contenu d'une page de produits, extrait les liens des produits, 
    puis utilise `write_product_data` pour écrire les informations de chaque produit 
    dans un fichier JSON.

    Args:
        session (aiohttp.ClientSession): La session HTTP pour les requêtes.
        url (str): L'URL de la page de produits à scraper.
        json_file (aiofiles file): Le fichier JSON où écrire les données.
    """
    html_content = await fetch_page(session, url)
    if html_content:
        product_links = await extract_product_links(html_content)
        await write_product_data(session, product_links, json_file, url)