from customtkinter import *
from tkinter import filedialog
from PIL import Image
import shutil
import webbrowser
from sources.scrapInfos import scrapInfos
from sources.test import final_res
import os

# Image folder clearing from start
folder = 'data/image'
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path) or os.path.islink(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)
    except Exception as e:
        print('Failed to delete %s. Reason: %s' % (file_path, e))

# Theme
set_appearance_mode("dark") 
set_default_color_theme("blue")  

copy_path = ""
file_path = ""

# Main window
window = CTk()
window.title("ReverseImage")
window.geometry("1000x650")
window.configure(bg="#1E1E1E")
window.grid_columnconfigure((0, 1), weight=1, uniform="a")
window.grid_rowconfigure(0, weight=1, uniform="a")

# Function to import the image with the button
def import_file():
    global copy_path, file_path
    file_path = filedialog.askopenfilename(title="Select an image", filetypes=[("Image files", "*.jpeg;*.jpg;*.png;*.gif"), ("All files", "*.*")])
    if file_path:
        print("Selected file:", file_path)
        copy_path = shutil.copy(src=file_path, dst="data/image")
        print(copy_path)
        
        image = CTkImage(light_image=Image.open(copy_path), dark_image=Image.open(copy_path), size=(250, 250))
        imageLabel.configure(text="", image=image)
        imageLabel.image = image
        
        imageScrap = Image.open(copy_path)
        try:
            data = scrapInfos(final_res(imageScrap))
        except:
            data = "No match found."
        print(data)
        
        if "error" in data:
            formatted_data = data["error"]
        else:
            oeuvre = data.get("OEUVRE", {})
            artiste = data.get("ARTISTE", {})
            formatted_data = (
                rf"""
                 ____                                 _         _   
                |  _ \ _____   _____ _ __ ___  ___   / \   _ __| |_ 
                | |_) / _ \ \ / / _ \ '__/ __|/ _ \ / _ \ | '__| __|
                |  _ <  __/\ V /  __/ |  \__ \  __// ___ \| |  | |_ 
                |_| \_\___| \_/ \___|_|  |___/\___/_/   \_\_|   \__|
                                                                    
                ────────────────────────────────────────────────────
                📜 𝐎𝐄𝐔𝐕𝐑𝐄
                ────────────────────────────────────────────────────
                🎫 Name: {oeuvre.get('nomOeuvre', 'N/A')}
                📅 Date: {oeuvre.get('date', 'N/A')}
                🏦 Exhibition Place: {oeuvre.get('lieuExposition', 'N/A')}
                🎨 Style: {oeuvre.get('style', 'N/A')}
                📏 Dimension: {oeuvre.get('dimension', 'N/A')}

                👨‍🎨 𝐀𝐑𝐓𝐈𝐒𝐓𝐄
                ────────────────────────────────────────────────────
                👤 Name: {artiste.get('nomArtiste', 'N/A')}
                🎂 Birth Date: {artiste.get('birthArtiste', 'N/A')}
                📍 Birth Place: {artiste.get('birthPlace', 'N/A')}
                ⚰️ Death Date: {artiste.get('deathArtiste', 'N/A')}
                🏡 Death Place: {artiste.get('deathPlace', 'N/A')}
                🌍 Nationality: {artiste.get('nationality', 'N/A')}
                """
            )
            
        textBox.configure(state="normal")
        textBox.delete("1.0", "end")  
        textBox.insert("1.0", formatted_data)
        textBox.configure(state="disabled")
        
        

# Function to open GitHub page
def open_github():
    webbrowser.open("https://github.com/Nnova13/2025_1093_revers-art")

# Left panel for image selection
leftFrame = CTkFrame(window, corner_radius=10)
leftFrame.grid(row=0, column=0, sticky=NSEW, padx=20, pady=20)
leftFrame.grid_columnconfigure(0, weight=1)
leftFrame.grid_rowconfigure((0, 1), weight=1)

# Image display label
imageLabel = CTkLabel(leftFrame, text="Select an image", anchor="center", fg_color="#2A2D2E", height=250, width=250, corner_radius=10)
imageLabel.grid(row=0, column=0, padx=20, pady=20)

# Import button
importButton = CTkButton(leftFrame, text="Upload Image", command=import_file, height=50, corner_radius=10, font=("Arial", 14, "bold"))
importButton.grid(row=1, column=0, padx=20, pady=20, sticky=EW)

# GitHub button
githubButton = CTkButton(leftFrame, text="Visit GitHub", command=open_github, height=30, corner_radius=10, font=("Arial", 10, "bold"))
githubButton.grid(row=2, column=0, padx=5, pady=5, sticky=EW)

# Right panel for displaying results/text
textFrame = CTkFrame(window, corner_radius=10)
textFrame.grid(row=0, column=1, sticky=NSEW, padx=20, pady=20)
textFrame.grid_columnconfigure(0, weight=1)
textFrame.grid_rowconfigure(0, weight=1)

textBox = CTkTextbox(
    textFrame, 
    wrap="word",  # Retour à la ligne automatique
    font=("Arial", 20),
    fg_color="#2A2D2E",
    text_color="white",
    corner_radius=10,
    height=500,  # Ajuster la hauteur selon l'interface
)
textBox.grid(row=0, column=0, padx=20, pady=20, sticky=NSEW)

# Ajouter du texte dans la Textbox
textBox.insert("1.0", "Bienvenue sur ReverseImage!\n")
textBox.configure(state="disabled")  # Désactiver l'édition

window.mainloop()