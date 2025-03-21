# 🏆 Documentation technique — Projet NSI : *Revers-Art*

Bienvenue dans la documentation du projet **Revers-Art**.  
Ce fichier explique la **structure du projet**, le **rôle des fichiers**, et l’**organisation du code**, pour permettre à n'importe quel élève de reprendre facilement le projet.

---

## 🌳 Structure

```text
2025_1093_revers-art/
│   licence.txt              ← Licence du projet
│   README.md                ← Présentation générale
│   requirements.txt         ← Bibliothèques Python nécessaires
│
├───data/                    ← 💾 Données utilisées par le projet
│   ├── crawler.json         ← Base de donée avec hash des images
│
├───docs/                    ← 📚 Documentation technique
│   ├── PROJETINFOS.md       ← Ce fichier
│
└───sources/                 ← 💻 Code source principal
    │   crawler.py           ← Script de récupération de données (pour la base de donées)
    │   main.py              ← Lanceur principal du programme (serveur Flask)
    │   scrapInfos.py        ← Fonctions de scraping
    │   test.py              ← Trouve l'image dans la base de donnée avec la hash
    │
    ├───reves-art-app/       ← 🧩 Application Tkinter
    │   └── app.py           ← Lanceur de l'application
    │
    ├───static/              ← 🎨 Fichiers statiques
    │   └───css/             ← Dossier css
    │       ├── error.css    ← Style page error
    │       ├── index.css    ← Style page index
    │       └── oeuvre.css   ← Style page oeuvre
    │
    └───templates/           ← 🖼️ Modèles HTML
        ├── error.html       ← Page erreur
        ├── index.html       ← Page principale
        └── oeuvre.html      ← Page d'affichage des résulats
```

## ⚙️ Schéma de fonctionnement du projet
```
crawler.json ◄─► test.py ◄─► scrapInfos.py
                                  │
                                  ▼
                              main.py (Flask)
                                  │
                ┌─────────────────┴─────────────────┐
                ▼                                   ▼
          templates/ (HTML)                static/css (styles)
```