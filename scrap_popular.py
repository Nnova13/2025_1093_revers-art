import requests
from bs4 import BeautifulSoup

# URL de la page à scraper
url = 'https://www.wikiart.org/fr/popular-paintings/alltime'

# Envoi de la requête HTTP pour récupérer le contenu de la page
response = requests.get(url)
response.raise_for_status()  # Vérifie que la requête s'est bien passée

# Analyse du contenu HTML avec BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Liste pour stocker les résultats
oeuvres = []

# Recherche des balises contenant les informations des œuvres
# Supposons que chaque œuvre est dans une balise <li> avec une classe spécifique
for li in soup.find_all('li', class_='painting-list-text-row'):
    a_tag = li.find('a')
    if a_tag and 'href' in a_tag.attrs:
        page_url = a_tag['href']
        # Construction de l'URL complète si nécessaire
        if not page_url.startswith('http'):
            page_url = 'https://www.wikiart.org' + page_url
        # Recherche de l'image associée
        img_tag = a_tag.find('img')
        if img_tag and 'src' in img_tag.attrs:
            img_url = img_tag['src']
            # Ajout des informations à la liste
            oeuvres.append({'page_url': page_url, 'img_url': img_url})

# Affichage des résultats
for oeuvre in oeuvres:
    print(f"Page URL: {oeuvre['page_url']}, Image URL: {oeuvre['img_url']}")
