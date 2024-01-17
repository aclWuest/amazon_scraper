
import asyncio
import aiofiles
import aiohttp
import time
from .config import RECHERCHE, ORDRE_CROISSANT, ELIGIBLE_LIVRAISON_GRATUITE, QUATRE_ETOILE, LIMIT
from .utils import construct_search_url,get_increment
from .scraper import scrape_product_page_generator, find_total_pages

async def main():
    """
    Fonction principale asynchrone pour orchestrer le processus de scraping.

    Cette fonction configure et initie le processus de scraping des produits sur Amazon.
    Elle construit l'URL de recherche basée sur les critères spécifiés dans `config.py`,
    puis lance le processus de scraping sur les pages de résultats obtenues. Les données 
    extraites de chaque produit sont écrites dans un fichier JSON. 
    Elle gère également la session HTTP et le fichier de sortie, s'assurant que toutes 
    les ressources sont correctement gérées.

    Le processus inclut :
    - La création d'une session HTTP asynchrone pour toutes les requêtes réseau.
    - L'ouverture d'un fichier JSON pour stocker les résultats.
    - La construction de l'URL de recherche Amazon avec les critères spécifiés.
    - Le scraping de chaque page de produits trouvée.
    - L'écriture des données extraites dans le fichier JSON.
    - La fermeture propre du fichier JSON et de la session HTTP à
    la fin du processus.

    Cette fonction utilise `asyncio` pour gérer les opérations asynchrones, permettant
    un scraping efficace et rapide sans bloquer l'exécution du programme pendant que les 
    requêtes réseau sont en cours.

    Note: Cette fonction est le point d'entrée du script lorsqu'exécuté en tant que package.
    """
    global initial_page_url
    initial_page_url = construct_search_url(
        'https://www.amazon.fr/s?k=', 
        RECHERCHE, 
        ORDRE_CROISSANT, 
        ELIGIBLE_LIVRAISON_GRATUITE, 
        QUATRE_ETOILE
    )

    async with aiohttp.ClientSession() as session, aiofiles.open('resultats.json', 'w',encoding="utf-8") as json_file:
        await json_file.write('[')
        total_pages = await find_total_pages(session, initial_page_url)
        tasks = []

        for page in range(1, total_pages + 1):
            page_url = initial_page_url + f'&page={page}'
            if get_increment() >= LIMIT:
                break
            await scrape_product_page_generator(session, page_url, json_file)

        current_position = await json_file.tell()
        await json_file.seek(current_position - 2) 
        await json_file.write('\n]')


if __name__ == "__main__":
    start = time.perf_counter()
    asyncio.run(main())
    stop = time.perf_counter()
    print(f"The extraction took {stop - start}")
