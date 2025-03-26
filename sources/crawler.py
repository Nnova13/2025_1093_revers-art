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
import time

FICHIER_HASHES = os.path.join(os.path.dirname(__file__), '../data/crawler.json')
MAX_THREADS = 15
BASE_URL = "https://www.wikiart.org"
RANDOM_URL = f"{BASE_URL}/fr/random"
verrou = threading.Lock()
stop_event = threading.Event()

def sauvegarder_hashes(nouveaux_hashes):
    """Ajoute les nouveaux hashes au fichier JSON de manière sécurisée."""
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

        fichier_temp = FICHIER_HASHES + ".tmp"
        with open(fichier_temp, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())

        os.replace(fichier_temp, FICHIER_HASHES)

def extraire_infos(soup):
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

        return html.unescape(artiste), html.unescape(oeuvre), img_url
    except Exception as e:
        print(f"❌ Erreur extraction infos : {e}")
        return "Inconnu", "Inconnu", None

def hacher_image():
    """Récupère une image aléatoire sur WikiArt, calcule son hash et l'enregistre."""
    try:
        r = requests.get(RANDOM_URL, timeout=10, allow_redirects=True)
        if r.status_code != 200:
            print(f"⚠️ Erreur HTTP {r.status_code}")
            return

        url_page = r.url
        soup = BeautifulSoup(r.content, "html.parser")
        artiste, oeuvre, img_url = extraire_infos(soup)

        if not img_url:
            print(f"❌ Aucune image trouvée sur {url_page}")
            return

        img_res = requests.get(img_url, timeout=10)
        if img_res.status_code != 200:
            print(f"⚠️ Erreur téléchargement image {img_url}")
            return

        img = Image.open(BytesIO(img_res.content)).convert("RGB")
        if min(img.size) < 100:
            print(f"❌ Image trop petite sur {url_page}")
            return

        img_resized = img.resize((256, 256))
        hash_image = str(imagehash.average_hash(img_resized))

        data = {"url_page": url_page, "hash": hash_image, "artiste": artiste, "oeuvre": oeuvre}
        sauvegarder_hashes([data])
        print(f"✅ Ajouté : {artiste} - {oeuvre} ({url_page})")

    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erreur réseau : {e}")
    except Exception as e:
        print(f"❌ Erreur de traitement : {e}")

def worker():
    """Thread qui exécute le crawler en continu tant que l'arrêt n'est pas demandé."""
    while not stop_event.is_set():
        hacher_image()
        time.sleep(0.5)  # Ajout d'une pause pour éviter les requêtes excessives

def crawler_art():
    """Démarre le crawler avec des threads et une gestion propre de l'arrêt."""
    print("🚀 Démarrage du crawler (CTRL+C pour arrêter)...")

    threads = [threading.Thread(target=worker, daemon=True) for _ in range(MAX_THREADS)]
    for t in threads:
        t.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Arrêt du crawler demandé. Fermeture des threads...")
        stop_event.set()
        for t in threads:
            t.join()
        print("✅ Crawler arrêté proprement.")

crawler_art()
