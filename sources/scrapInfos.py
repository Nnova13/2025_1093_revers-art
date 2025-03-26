from bs4 import BeautifulSoup
import requests

def scrapInfos(url:str):
    """Récupère les infos sur les oeuvres et l'artiste en question"""
    oeuvrePage = requests.get(url)

    oeuvreSoup = BeautifulSoup(oeuvrePage.text, "html.parser")

    ###########################################################
    ###################### INFOS  OEUVRE ######################
    ###########################################################

    try:
        nomOeuvre = oeuvreSoup.find('h3').text
    except:
        nomOeuvre = "Non défini"
    try:
        date = oeuvreSoup.find("span", itemprop='dateCreated').text
    except:
        date = "Non défini"
    try:
        lieuExposition = oeuvreSoup.find("li", class_="dictionary-values-gallery").find("span").text
    except:
        lieuExposition = "Non défini"
    try:
        style = oeuvreSoup.find('li', class_='dictionary-values').find('span').find('a').text
    except:
        style = "Non défini"
    try:
        dimension = str(oeuvreSoup.find('s', class_='title').parent.contents[2]).strip()
    except:
        dimension = "Non défini"
    try:
        imageUrl = oeuvreSoup.find('img', itemprop='image')['src']
    except:
        imageUrl = ""

    ###########################################################
    ###################### INFOS ARTISTE ######################
    ###########################################################

    linkArtistePage = 'https://www.wikiart.org'+oeuvreSoup.find("span", itemprop="name").find('a')["href"]

    artistePage = requests.get(linkArtistePage)
    artisteSoup = BeautifulSoup(artistePage.text, "html.parser")

    try:
        nomArtiste = str(artisteSoup.find('h3').text).strip()
    except:
        nomArtiste = "Non défini"

    try:
        birthArtiste = artisteSoup.find('span', itemprop = "birthDate").text
    except:
        birthArtiste = "Non défini"
    try:
        birthPlace = artisteSoup.find('span', itemprop = "birthPlace").text
    except:
        birthPlace = "Non défini"
    try:
        deathArtiste = artisteSoup.find('span', itemprop = "deathDate").text
    except:
        deathArtiste = "Non défini"
    try:
        deathPlace = artisteSoup.find('span', itemprop = "deathPlace").text
    except:
        deathPlace = "Non défini"
    try:
        nationality = artisteSoup.find('span', itemprop = "nationality").text
    except:
        nationality = "Non défini"

    data = {
        "OEUVRE":{
            "nomOeuvre":nomOeuvre,
            "date":date,
            "lieuExposition":lieuExposition,
            "style": style,
            "dimension":dimension,
            "imageUrl":imageUrl
            },
        "ARTISTE":{
            "nomArtiste":nomArtiste,
            "birthArtiste":birthArtiste,
            "birthPlace":birthPlace,
            "deathArtiste": deathArtiste,
            "deathPlace":deathPlace,
            "nationality":nationality}}
    return data
