# Projet de Scraping Amazon

## WARNING
La classe Product n'a que très peu de champ, je n'ai pas eu le temps d'en implémenter plus, car je me suis focalisé plus sur les concepts que je maîtrisais moins que le traitement de la donnée. J

Pour le moment, le fichier renvoyé en sortie est un JSON et non un CSV comme demandé. Ces modifications vont arriver avec la création de la classe dans la soirée.

De plus, la gestion des erreurs est quasi inexistante pour le moment et la rotation de proxy n'a pas encore été implémentée dans cette version à cause de problème lié à aiohttp ce qui m'a coûté énormément de temps. Ce sera fait ce soir également.

Je tiens à m'excuser pour ces petits retards, mais je n'ai eu qu'une nuit et demie nuit pour faire ce scraper comme je n'ai pas pu me libérer ce weekend et que je suis toujours en poste...

En espérant que ce soit suffisant pour vous prouver que j'apprends vite et que je suis motivé. Bonne lecture. 

## Description
Ce projet est un script de scraping asynchrone conçu pour extraire les données de produits depuis Amazon. Il utilise `aiohttp` pour les requêtes asynchrones et `BeautifulSoup` pour l'analyse du HTML.

## Fonctionnalités
- Recherche de produits sur Amazon avec des critères spécifiques (comme ordre croissant, livraison gratuite, etc.).
- Extraction asynchrone des données des produits.
- Stockage des informations de produit dans un fichier JSON.

## Prérequis
- Python 3.6 ou plus récent.
- Bibliothèques `aiohttp`, `aiofiles`, `beautifulsoup4`, `lxml`.

## Installation
Clonez ce dépôt en utilisant Git :
```bash
git clone https://github.com/votre_nom_utilisateur/votre_projet.git
cd votre_projet
```

Installez les dépendances :

```bash
Copy code
pip install aiohttp aiofiles beautifulsoup4 lxml fake_useragent
```

## Structure du Projet
Le projet est structuré en plusieurs modules :
- `main.py` : Point d'entrée du script.
- `scraper.py` : Contient la logique de scraping.
- `utils.py` : Fonctions utilitaires.
- `config.py` : Configuration et constantes.

## Exécution en tant que Package
Pour exécuter ce projet en tant que package, suivez les étapes ci-dessous :

1. **Organisez le code en structure de package :**
   Assurez-vous que votre projet est structuré comme un package Python. Votre structure de dossiers devrait ressembler à ceci :

votre_projet/
├── amazon_scraper/
│   ├── __init__.py
│   ├── main.py
│   ├── scraper.py
│   ├── utils.py
│   └── config.py
└── README.md

2. **Ajout d'un `__init__.py` :**
Créez un fichier `__init__.py` vide dans le dossier `amazon_scraper`. Ce fichier est nécessaire pour que Python traite le dossier comme un package.

3. **Exécution du package :**
Placez-vous dans le répertoire parent de `amazon_scraper` (c'est-à-dire dans `votre_projet/`) et exécutez le package avec la commande suivante :
```bash
python -m amazon_scraper.main
```
## Utilisation
Pour utiliser ce script de scraping, suivez ces étapes :

1. **Configurer les Critères de Recherche :**
   - Ouvrez le fichier `config.py`.
   - Modifiez les variables pour définir vos critères de recherche. Par exemple, changez la valeur de `RECHERCHE` pour spécifier le produit à rechercher sur Amazon.

2. **Lancer le Script :**
   - Assurez-vous d'être dans le répertoire racine du package `amazon_scraper`.
   - Exécutez le script en utilisant la commande suivante :
     ```bash
     python -m amazon_scraper.main
     ```

3. **Résultats :**
   - Le script va scraper les données des produits selon vos critères de recherche et les enregistrer dans un fichier JSON nommé `products_feed.json`.
   - Vous pouvez trouver ce fichier dans le même répertoire que le script `main.py`.

### Paramètres Configurables
Dans `config.py`, vous pouvez configurer les paramètres suivants :
- `RECHERCHE`: Le terme de recherche à utiliser sur Amazon.
- `ORDRE_CROISSANT`: Définir sur `True` pour trier les résultats par ordre de prix croissant.
- `ELIGIBLE_LIVRAISON_GRATUITE`: Définir sur `True` pour filtrer les produits éligibles à la livraison gratuite.
- `QUATRE_ETOILE`: Définir sur `True` pour filtrer les produits ayant quatre étoiles et plus.

Notez que ce script est conçu pour une utilisation éducative et de démonstration. Assurez-vous de respecter les conditions d'utilisation d'Amazon et les lois sur le scraping de données.
