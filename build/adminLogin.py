import tkinter as tk
from tkinter import Canvas, PhotoImage, Entry, Button, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from datetime import datetime
from ttkbootstrap.widgets import DateEntry
from PIL import Image, ImageTk
import mysql.connector
import pandas as pd
from script import indicatifs,pays_indicatifs
from subprocess import call, Popen
from session_manager import SessionManager
import tkinter as tk
import webbrowser
from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\images")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Fonction pour ouvrir le lien
def open_webpage():
    url = "http://127.0.0.1:8050/"  # Remplacez par l'URL de votre choix
    webbrowser.open(url)
        

user="admin"
pwd="admin"

    
class Login(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Login")
        self.setup_ui()
        
    def setup_ui(self):
        # Frame principal
        
        self.logFrame = ttk.Frame(self)
        self.logFrame.pack(expand=True)
        
        # Chargement de l'image
        image = Image.open(relative_to_assets("retour.png"))  # Remplacez par le chemin correct
        image = image.resize((20, 20))  # Redimensionner l'image
        self.img1 = ImageTk.PhotoImage(image)  # Garder une référence


        
        self.titre = ttk.Label(self.logFrame,text="Accès au tableau de bord! !",font=("Inter SemiBold", 13))
        self.titre.grid(row=0,column=0, sticky="nsew", pady=10, padx=(35,10))
        
        # Champs et entrée
        
        self.secFrame = ttk.Frame(self.logFrame)
        self.secFrame.grid(row=2, column=0, padx=10, sticky="nsew")
        
        self.email = ttk.Label(self.secFrame, text="Non utilisateur",font=("Inter SemiBold", 8))
        self.email.grid(row=0, column=0,padx=(10, 20), pady=(10, 5), sticky="w")
        
        self.entry_email = ttk.Entry(self.secFrame, bootstyle="info")
        self.entry_email.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 20), ipadx=50)
        
        self.mdp = ttk.Label(self.secFrame, text="Mot de passe", font=("Inter", 8))
        self.mdp.grid(row=2, column=0, padx=(10, 20), pady=(10, 5), sticky="w")

        self.entry_password = ttk.Entry(self.secFrame, bootstyle="info", show="*")
        self.entry_password.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 20), ipadx=50)
        
        
        # Button
        
        self.button_login = ttk.Button(
            self.logFrame,
            text="Suivant",
            bootstyle=INFO,
            command=self.verification
        )
        self.button_login.grid(row=3, column=0, pady=10, ipadx=30, ipady=5,padx=(0,10))
        
        
        
        self.logFrame.grid_rowconfigure(0, weight=1)
        self.logFrame.grid_rowconfigure(1, weight=1)
        self.logFrame.grid_columnconfigure(0, weight=1)
    
    def register(self):
        self.destroy()
        call(["python", "Register_class.py"])
        
    def verification(self):
        email= self.entry_email.get()
        mdp = self.entry_password.get()
        
        if email==user and mdp==pwd:
            
            messagebox.showinfo("Succès", "Bienvenue !") 
            self.destroy()
            # Lance Dash.py en arrière-plan
            Popen(["python", "Dash.py"])
            # Ouvre le navigateur
            open_webpage()
        else:messagebox.showerror("Erreur", "Email ou mot de passe incorrect.")


    
        
if __name__ == "__main__":
    app = Login()
    app.mainloop()
