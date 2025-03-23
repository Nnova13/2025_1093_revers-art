import json
import imagehash
import os.path

FICHIER_JSON = os.path.abspath('./data/crawler.json')

def charger_hashes():
    """Charge la base de données des hashes depuis le fichier JSON."""
    try:
        with open(FICHIER_JSON, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def phash_image(image):
    """Calcule le hash perceptuel (average hash) de l'image."""
    return imagehash.average_hash(image)

def rechercher_image_pil(image, seuil_hamming=18):
    """Recherche une image PIL dans la base avec une distance de Hamming."""
    base_hashes = charger_hashes()
    if not base_hashes:
        print("🚨 Aucune base de données d'images trouvée.")
        return None

    new_hash = phash_image(image)
    meilleure_correspondance = None
    distance_minimale = seuil_hamming + 1

    for h in base_hashes:
        hash_image = imagehash.hex_to_hash(h["hash"])
        distance = new_hash - hash_image

        if distance == 0:
            return h 

        if distance < distance_minimale:
            distance_minimale = distance
            meilleure_correspondance = h

    if meilleure_correspondance and distance_minimale <= seuil_hamming:
        return meilleure_correspondance

    print("❌ Aucune correspondance trouvée.")
    return None

def final_res(image_test, seuil=18):
    resultat = rechercher_image_pil(image_test, seuil)
    if resultat:
        print(f"🔎 Infos de l'œuvre trouvée :\n • 🌐 url : {resultat['url_page']}\n • 🧬 hash : {resultat['hash']}\n • 🖼️ oeuvre : {resultat['oeuvre']}\n • 🎨 artiste : {resultat['artiste']}")
        return resultat['url_page']