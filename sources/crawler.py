import requests
from bs4 import BeautifulSoup
import imagehash
import json
import os
import threading
from queue import Queue
from PIL import Image
from io import BytesIO
import html


FICHIER_HASHES = os.path.join(os.path.dirname(__file__), '../crawler.json')
MAX_THREADS = 30
BASE_URL = "https://www.wikiart.org"
RANDOM_URL = f"{BASE_URL}/fr/random"
verrou = threading.Lock()
file_urls = Queue()

def sauvegarder_hashes(nouveaux_hashes):
    """Ajoute les nouveaux hashes au fichier JSON s'ils ne sont pas déjà enregistrés."""
    with verrou:
        if os.path.exists(FICHIER_HASHES):
            try:
                with open(FICHIER_HASHES, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = []
        else:
            data = []

        for h in nouveaux_hashes:
            if not any(d["hash"] == h["hash"] for d in data):
                data.append(h)

        with open(FICHIER_HASHES, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

def extraire_infos(soup, url_page):
    """Extrait le nom de l'artiste et de l'œuvre à partir du HTML."""
    try:
        img_tag = soup.find("img", itemprop="image")
        img_url = img_tag["src"] if img_tag else None

        script_tag = soup.find("div", class_="wiki-layout-painting-info-bottom")
        if script_tag:
            json_str = script_tag["ng-init"].split("=", 1)[-1].strip().rstrip(";")
            json_data = json.loads(json_str.replace("&quot;", "\""))
            artiste = json_data.get("artistName", "Inconnu")
            oeuvre = json_data.get("title", "Inconnu")
        else:
            artiste, oeuvre = "Inconnu", "Inconnu"
        
        artiste = html.unescape(artiste)
        oeuvre = html.unescape(oeuvre)
        return artiste, oeuvre, img_url
    except Exception as e:
        print(f"❌ Erreur extraction infos : {e}")
        return "Inconnu", "Inconnu", None

def hacher_image():
    """Fait une requête vers /random, suit la redirection, et extrait les infos de l'œuvre."""
    try:
        r = requests.get(RANDOM_URL, timeout=5, allow_redirects=True)
        if r.status_code != 200:
            return

        url_page = r.url  
        soup = BeautifulSoup(r.content, "html.parser")
        artiste, oeuvre, img_url = extraire_infos(soup, url_page)

        if not img_url:
            print(f"❌ Aucune image trouvée sur {url_page}")
            return

        img_res = requests.get(img_url, timeout=5)
        if img_res.status_code == 200:
            img = Image.open(BytesIO(img_res.content)).convert("RGB")

            if min(img.size) < 100:
                print(f"❌ Image trop petite sur {url_page}")
                return
            
            img_resized = img.resize((256, 256)) 
            hash_image = str(imagehash.average_hash(img_resized))

            data = {"url_page": url_page, "hash": hash_image, "artiste": artiste, "oeuvre": oeuvre}
            sauvegarder_hashes([data])
            # print(f"✅ Ajout : {artiste} - {oeuvre} ({url_page})")

    except Exception as e:
        print(f"❌ Erreur de traitement :", e)

def worker():
    """Thread qui tourne en boucle infinie pour traiter les images en continu."""
    while True:
        hacher_image()

def crawler_art():
    """Démarre le crawler multithread pour tourner en continu."""
    print("🚀 Démarrage du crawler (CTRL+C pour arrêter)...")

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(MAX_THREADS)]

    for t in threads:
        t.start()

    try:
        while True: 
            pass
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du crawler demandé. Fermeture des threads...")
        os._exit(0) 

crawler_art()