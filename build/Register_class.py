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
from subprocess import call



def Accueil():
    app.destroy()
    call(["python", "Accueil_01.py"])

def connect_to_database():
    'Cette fonction permet de se connecter à la base de donnée'
    try:
        global conn, cursor
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="e_commerce"
        )
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        messagebox.showerror("Error", f"Error connecting to database: {e}")
        

connect_to_database() #Connecter la base

class Register(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("900x600")
        self.title("Register")
        
        self.setup_ui()
        
    def setup_ui(self):
        # Création du Notebook (gestionnaire d'onglets)
        self.multipage = ttk.Notebook(self)
        style = ttk.Style()
        style.layout('TNotebook.Tab', []) # turn off tabs
        note = ttk.Notebook(self)
        self.multipage.pack(fill=tk.BOTH, expand=True)
        
        self.page1 = ttk.Frame(self.multipage)
        self.multipage.add(self.page1, text="")
        
        self.page2 = ttk.Frame(self.multipage)
        self.multipage.add(self.page2, text="")
        
        self.page3 = ttk.Frame(self.multipage)
        self.multipage.add(self.page3, text="")
        
        self.setup_page1()
        self.setup_page2()
        self.setup_page3()
    
    

    def setup_page1(self):
        # Conteneur principal pour centrer tout verticalement
        self.page1_container = ttk.Frame(self.page1)
        self.page1_container.pack(expand=True)  

        

        # Texte 1
        self.p1texte1 = ttk.Label(self.page1_container, text="Bienvenue", font=("Inter SemiBold", 16))
        self.p1texte1.pack(pady=10)

        # Texte 2
        self.p1texte2 = tk.Label(
            self.page1_container,
            text="Entrez votre adresse email pour amorcer\nle processus de création de votre compte",
            font=("Inter", 9),
        )
        self.p1texte2.pack(pady=10)

        # Champ de saisie email
        self.entry_email = ttk.Entry(self.page1_container, bootstyle="info")
        self.entry_email.pack(pady=20, ipadx=100, ipady=5)  

        self.button_next1 = ttk.Button(
            self.page1_container,
            text="Suivant",
            bootstyle=SUCCESS,
            command=self.valid1
        )
        self.button_next1.pack(pady=20,padx=10, ipadx=50, ipady=5)


    def setup_page2(self):
        # Chargement de l'image
        image = Image.open(r".\assets\frame_01Ac\image_13.png")  # Remplacez par le chemin correct
        image = image.resize((20, 20))  # Redimensionner l'image
        self.img1 = ImageTk.PhotoImage(image)  # Garder une référence

        # Bouton "Retour" placé dans le coin supérieur gauche
        self.button_back1 = ttk.Button(
            self.page2,
            image=self.img1,
            bootstyle=SUCCESS,
            command=lambda: self.multipage.select(0),
        )
        self.button_back1.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nw")

        # Conteneur principal centré
        self.page2_contener = ttk.Frame(self.page2)
        self.page2_contener.grid(row=1, column=0, padx=10, sticky="nsew")

        # Centrer verticalement et horizontalement
        self.page2.grid_rowconfigure(0, weight=1)
        self.page2.grid_rowconfigure(1, weight=1)
        self.page2.grid_columnconfigure(0, weight=1)

        # Contenu du conteneur
        self.p2texte1 = ttk.Label(self.page2_contener, text="Créer votre compte", font=("Inter SemiBold", 16))
        self.p2texte1.pack(pady=10)

        self.p2texte2 = ttk.Label(
            self.page2_contener,
            text="Pour assurer la sécurité de votre compte, veuillez entrer un",
            font=("Inter", 9)
        )
        self.p2texte2.pack(pady=(10, 0))

        self.p2texte3 = ttk.Label(
            self.page2_contener,
            text="mot de passe d’au moins 8 caractères.",
            font=("Inter", 9)
        )
        self.p2texte3.pack(pady=(3, 10))

        # Conteneur pour organiser les champs
        self.fields_frame = ttk.Frame(self.page2_contener)
        self.fields_frame.pack(pady=20)

        # Mot de passe
        self.mdp = ttk.Label(self.fields_frame, text="Mot de passe", font=("Inter", 9))
        self.mdp.grid(row=0, column=0, padx=(10, 20), pady=(10, 5), sticky="w")

        self.entry_password = ttk.Entry(self.fields_frame, bootstyle="info", show="*")
        self.entry_password.grid(row=1, column=0, columnspan=2, padx=10, pady=(5, 20), ipadx=50)

        # Confirmation du mot de passe
        self.mdpc = ttk.Label(self.fields_frame, text="Confirmation mot de passe", font=("Inter", 9))
        self.mdpc.grid(row=2, column=0, padx=(10, 20), pady=(10, 5), sticky="w")

        self.entry_password_confirm = ttk.Entry(self.fields_frame, bootstyle="info", show="*")
        self.entry_password_confirm.grid(row=3, column=0, columnspan=2, padx=10, pady=(5, 20), ipadx=50)

        # Boutons
        self.BoutFrame = ttk.Frame(self.page2_contener)
        self.BoutFrame.pack(pady=0)

        self.button_next2 = ttk.Button(
            self.BoutFrame,
            text="Suivant",
            bootstyle=SUCCESS,
            command=self.valid2
        )
        self.button_next2.grid(row=0, column=0, pady=10, ipadx=50, ipady=5)
        
        

    def setup_page3(self):
        # Chargement de l'image
        image = Image.open(r".\assets\frame_01Ac\image_13.png")  # Remplacez par le chemin correct
        image = image.resize((20, 20))  # Redimensionner l'image
        self.img2 = ImageTk.PhotoImage(image)  # Garder une référence

        # Bouton "Retour" placé dans le coin supérieur gauche
        self.button_back2 = ttk.Button(
            self.page3,
            image=self.img2,
            bootstyle=SUCCESS,
            command=lambda: self.multipage.select(1),
        )
        self.button_back2.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        # Conteneur principal centré (sans étirement)
        self.page3_contener = ttk.Frame(self.page3)
        self.page3_contener.grid(row=1, column=0, padx=10, sticky="n", pady=20)

        # Centrer verticalement
        self.page3.grid_rowconfigure(0, weight=1)  # Espace pour la ligne du dessus
        self.page3.grid_rowconfigure(1, weight=0)  # Ligne contenant le conteneur, pas de poids d'étirement ici
        self.page3.grid_rowconfigure(2, weight=1)  # Espace pour la ligne du dessous

        self.page3.grid_columnconfigure(0, weight=1)  # Conteneur centré horizontalement

        self.p3texte1 = ttk.Label(self.page3_contener, text="Créer votre compte", font=("Inter SemiBold", 16))
        self.p3texte1.grid(row=0, column=0, columnspan=2, pady=0)

        self.p3texte1 = ttk.Label(
            self.page3_contener,
            text="Nous y sommes presque, apprenez-nous-en plus sur vous !",
            font=("Inter", 9)
        )
        self.p3texte1.grid(row=1, column=0, columnspan=2, pady=(7, 60))

        # Nom
        self.nom = ttk.Label(
            self.page3_contener,
            text="Nom",
            font=("Inter", 9)
        )
        self.nom.grid(row=2, column=0, sticky="w", padx=10)
        self.entry_nom = ttk.Entry(self.page3_contener, bootstyle="info")
        self.entry_nom.grid(row=3, column=0, pady=10, padx=10, sticky="ew", ipadx=60)

        # Prénom(s)
        self.prenom = ttk.Label(
            self.page3_contener,
            text="Prénom(s)",
            font=("Inter", 9)
        )
        self.prenom.grid(row=4, column=0, sticky="w", padx=10)
        self.entry_prenom = ttk.Entry(self.page3_contener, bootstyle="info")
        self.entry_prenom.grid(row=5, column=0, pady=10, padx=10, sticky="ew")

        # Numéro de téléphone
        self.tel = ttk.Label(
            self.page3_contener,
            text="Numéro de téléphone",
            font=("Inter", 9)
        )
        self.tel.grid(row=2, column=1, sticky="w", padx=20)

        self.tel_frame = ttk.Frame(self.page3_contener)  # Conteneur pour l'indicatif et le champ
        self.tel_frame.grid(row=3, column=1, pady=10, padx=20, sticky="ew")

        self.entry_indicatif = ttk.Combobox(self.tel_frame, width=5, bootstyle="info", values=list(pays_indicatifs.keys()))
        self.entry_indicatif.pack(side="left", padx=(0, 5), ipadx=5)  # Petite marge à droite
        self.entry_indicatif.bind("<<ComboboxSelected>>", self.mettre_indicatif)
        

        self.entry_tel = ttk.Entry(self.tel_frame, bootstyle="info")
        self.entry_tel.pack(side="left", fill="x", expand=True,ipadx=25)

        # Frame pour alignement de la date de naissance et du sexe
        self.sexe_birth = ttk.Frame(self.page3_contener)
        self.sexe_birth.grid(row=4, column=1, rowspan=2, columnspan=2)

        # Sexe
        self.sexe_label = ttk.Label(
            self.sexe_birth,
            text="Sexe",
            font=("Inter", 9)
        )
        self.selected_sexe = tk.StringVar(value="")
        self.sexe_label.grid(row=0, column=0, sticky="w", padx=10)
        self.sexe_frame = ttk.Frame(self.sexe_birth)  # Conteneur pour centrer les boutons
        self.sexe_frame.grid(row=1, column=0, sticky="ew", padx=10)
        self.sexe_homme = ttk.Radiobutton(self.sexe_frame, text="M", value="Masculin", variable=self.selected_sexe)
        self.sexe_homme.pack(side="left", padx=5)
        self.sexe_femme = ttk.Radiobutton(self.sexe_frame, text="F", value="Feminin", variable=self.selected_sexe)
        self.sexe_femme.pack(side="left", padx=5)

        # Date de naissance
        self.birth = ttk.Label(
            self.sexe_birth,
            text="Date de naissance",
            font=("Inter", 9)
        )
        self.birth.grid(row=0, column=1, sticky="w", padx=10)
        self.entry_birth = DateEntry(self.sexe_birth)
        self.entry_birth.grid(row=1, column=1, pady=10, padx=10, sticky="ew")

        # Conditions d'utilisation  

        self.conditions_frame = ttk.Frame(self.page3_contener)
        self.conditions_frame.grid(row=7, column=0, columnspan=2, pady=(10))
        self.conditions_var = ttk.BooleanVar(value=FALSE)
        self.conditions_check = ttk.Checkbutton(self.conditions_frame, variable=self.conditions_var, command=self.toggle_button_state)
        self.conditions_check.pack(side="left")
        self.conditions_text = ttk.Label(
            self.conditions_frame,
            text="En continuant, vous acceptez les ",
            font=("Inter", 8)
        )
        self.conditions_text.pack(side="left")
        self.conditions_link = ttk.Label(
            self.conditions_frame,
            text="conditions d'utilisation",
            font=("Inter", 8),
            foreground="blue",
            cursor="hand2"
        )
        self.conditions_link.pack(side="left")

        # Bouton créer
        self.button_submit = ttk.Button(
            self.page3_contener,
            text="Créer mon compte",
            bootstyle=SUCCESS,
            state="disabled",
            command=self.valid3
        )
        self.button_submit.grid(row=8, column=0, columnspan=2, pady=20, ipadx=7, ipady=5)

        # Ajout de stretch pour la grille
        self.page3_contener.grid_columnconfigure(0, weight=0)
        self.page3_contener.grid_columnconfigure(1, weight=0)
        
        
    #Les fonctions
        
    def toggle_button_state(self):
            if self.conditions_var.get(): 
                self.button_submit.config(state="normal")  
            else:
                self.button_submit.config(state="disabled")

    def mettre_indicatif(self,event):
                pays_selectionne = self.entry_indicatif.get()
                indicatif = pays_indicatifs.get(pays_selectionne, "")
                if indicatif:
                    self.entry_indicatif.delete(0, tk.END) 
                    self.entry_indicatif.insert(0, indicatif)  
                    
    def valid1(self):
        mail = self.entry_email.get()
        if not mail:
            messagebox.showerror("Erreur","Veuillez entrer une adresse email svp !")
            return False
        if "@" not in mail or "." not in mail:
            messagebox.showerror("Erreur","Veuillez entrer une adresse électronique valide !")
            return False
        self.multipage.select(1)
        return True
        
    
    def valid2(self):
        mdp = self.entry_password.get()
        cmdp = self.entry_password_confirm.get()
        if not mdp or not cmdp:
            messagebox.showerror("Erreur", "Veuillez remplir les deux champs de mot de passe !")
            return False
        if mdp!=cmdp:
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")
            return False
        if len(mdp) < 8:
            messagebox.showerror("Erreur", "Le mot de passe doit contenir au moins 8 caractères.")
            return False
        self.multipage.select(2)
        return True
        
    def valid3(self):
        nom = self.entry_nom.get()
        prenom = self.entry_prenom.get()
        indi = self.entry_indicatif.get()
        tel = self.entry_tel.get()
        birth = self.entry_birth.entry.get()
        sexe = self.selected_sexe.get()
        
        if not tel.isdigit():
            return messagebox.showerror("Erreur !", "Le numéro de téléphone doit être une série de chiffres !")
        
        if len(tel)>10 or len(tel)<8:
            return messagebox.showerror("Erreur !", "Le numéro entré est invalide !")
        if nom and prenom and indi and tel and birth and sexe:
            self.ajouter_client()
        else: 
            return messagebox.showerror("Erreur !", "Veuillez renseigner tous les champs pour continuer !")

        
    # Fonction pour insérer des données dans la table client
    def ajouter_client(self):
        nom = self.entry_nom.get()
        prenom =self.entry_prenom.get()
        email = self.entry_email.get()
        mdp = self.entry_password.get()
        tel = self.entry_indicatif.get() + " " + self.entry_tel.get() 
        birth_date = self.entry_birth.entry.get()
        sexe = self.selected_sexe.get()
        if nom and prenom and email and mdp and tel and birth_date and sexe:  
            # Convertir en objet datetime
            try:
                date_obj = datetime.strptime(birth_date, "%m/%d/%Y")  # Convertit la chaîne en objet datetime
                mysql_date = date_obj.strftime("%Y-%m-%d")  # Convertit l'objet datetime en format MySQL
                try:
                    query = "INSERT INTO client (nom, prenoms,sexe,date_naissance,email,mdp,numero_tel) VALUES (%s, %s,%s, %s,%s, %s,%s)"
                    values = (nom, prenom,sexe,mysql_date,email,mdp,tel)
                    cursor.execute(query, values)
                    conn.commit()

                    messagebox.showinfo("Succès", "Compte créer avec succès !")
                    app.destroy()
                    call(["python", "Accueil_01.py"])
                    
                except mysql.connector.Error as err:
                    messagebox.showerror("Erreur d'insertion", f"Erreur : {err}")
            except ValueError:
                messagebox.showwarning("Erreur","La date saisie n'est pas valide!")
            
        else:
            messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs !")
        

# Exécution de l'application
if __name__ == "__main__":
    app = Register()
    app.mainloop()
    
# class Confidential(tk.Tk):
#     def __init__(self):
#         super().__init__()
#         self.geometry("50x100")
#         self.title("Conditions de confidentialité")
#         self.frame = ttk.Frame(self)
#         self.frame.pack(expand=True)
#         self.texte = ttk.Label(self.frame,text="Le Directeur de Cabinet Adjoint, représentant du Ministre, à lui à son tour souhaité une bienvenue aux participants. Il a signifié qu’il était important pour un Etat d’avoir les statistiques fiables sur les naissances, les décès, les mariages et les divorces. Pour ce faire, Monsieur le Directeur de Cabinet Adjoint a encouragé les acteurs à l’amélioration des enregistrements de données d’état civil car, le signifiait-il, le taux d’enregistrement des données d’état civil est faible. Pour clore ces propos, le représentant du Ministre a déclaré ouverte l’atelier de présentation de l’annuaire statistique d’état civil 2017 et de son rapport d’analyse.")
#         self.texte.pack(padx=10, pady=10)