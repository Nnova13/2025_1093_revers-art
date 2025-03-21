from customtkinter import *
from tkinter import filedialog
from PIL import Image
import shutil
import webbrowser

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
        copy_path = shutil.copy(src=file_path, dst="./././data")
        print(copy_path)
        
        image = CTkImage(light_image=Image.open(copy_path), dark_image=Image.open(copy_path), size=(250, 250))
        imageLabel.configure(text="", image=image)
        imageLabel.image = image

# Function to open GitHub page
def open_github():
    webbrowser.open("https://github.com/nnova13/reverse-art")

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

# Textbox for displaying infos
textLabel = CTkTextbox(textFrame, wrap="word", font=("Arial", 12), fg_color="#2A2D2E", text_color="white", corner_radius=10)
textLabel.grid(row=0, column=0, padx=20, pady=20, sticky=NSEW)

window.mainloop()