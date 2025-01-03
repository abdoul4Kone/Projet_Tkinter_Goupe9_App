import tkinter
import tkinter as tk
from tkinter import messagebox
import tkinter.messagebox
import customtkinter 
# import ttkbootstrap as ttk
import mysql.connector
from pathlib import Path
from PIL import Image
# from ttkbootstrap.tableview import Tableview
from session_manager import user_id
import os
import json
from subprocess import call
from cryptography.fernet import Fernet
import json

# Génération d'une clé de chiffrement (ceci devrait être fait une seule fois et stocké de manière sécurisée)
key = Fernet.generate_key()
cipher_suite = Fernet(key)

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r".\assets\images")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

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

user_id = user_id #Récupération de l'id de l'utilisateur connecté
print(user_id)
def get_data(id):
    try:
        global user
        query = "SELECT nom, prenoms, sexe, date_naissance, email, mdp, numero_tel FROM Client WHERE id = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchone()  # Récupère une seule ligne
            
        if result:
            nom, prenoms, sexe, birth_date, email, mdp, tel = result
            user = ConnectedUser(nom, prenoms, sexe, birth_date, email, mdp, tel)
        else:
            messagebox.showerror("Erreur", "Utilisateur introuvable.")
    except mysql.connector.Error as err:
        messagebox.showerror("Erreur", f"Erreur de base de données : {err}")

        
class ConnectedUser:
    def __init__(self,nom, prenoms,sexe,birth_date,email,mdp,tel):
        self.nom = nom
        self.prenoms = prenoms
        self.sexe = sexe
        self.birth_date = birth_date
        self.email = email
        self.mdp = mdp
        self.tel = tel
   
def modifierPanier():
    app.destroy()
    call(["python", "Panier.py"])   
    
#Retour à l'acccueil      
def home(): 
    app.destroy()
    call(["python", "Accueil.py"])
        
get_data(user_id)
customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Commander(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("Commander")
        self.geometry(f"{1100}x{580}")
        
        
        
        self.setup_ui()

        # configure grid layout (4x4)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)
        
    def setup_ui(self):
        
        #Frame Principal
        
        # self.framePrincipal = customtkinter.CTkScrollableFrame(self,scrollbar_button_color="lightgrey")
        # self.framePrincipal.pack(fill=BOTH, expand=YES, padx=10, pady=10)
        
        #En-tête

        self.grid_columnconfigure((0,1), weight=2)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=0)
        self.entete = customtkinter.CTkFrame(self,fg_color="#fff", corner_radius=0,height=60)
        self.entete.grid(row=0, column=0,columnspan=2, padx=0, pady=0,sticky="nsew")
        
        customtkinter.CTkButton(self.entete,text=" ",width=100,corner_radius=0,fg_color="transparent", hover=False, command=home,image= customtkinter.CTkImage(light_image=Image.open(relative_to_assets('logo.png')), size=(70, 50))).grid(row=0,column=0, sticky="nsw", padx=40)
        customtkinter.CTkLabel(self.entete, text="Commander", font=customtkinter.CTkFont(size=18, weight="bold"),text_color="#1B6392").grid(row=0,column=1, sticky="e", padx=(640,5))
        customtkinter.CTkButton(self.entete,width=40, text=" ",fg_color="#1B6392", hover=False,image= customtkinter.CTkImage(light_image=Image.open(relative_to_assets('cart.png')), size=(30, 30))).grid(row=0,column=2, sticky="e", padx=(0,40))

        
        self.frameCommande = customtkinter.CTkScrollableFrame(self,corner_radius=0,fg_color="lightgrey",scrollbar_button_color="lightgrey")
        self.frameCommande.grid(row=1, column=0,columnspan=2, padx=0, pady=(0,10),sticky="nsew")
        
        #Info client
        self.InfoFrame = customtkinter.CTkFrame(self.frameCommande, width=770,fg_color="#fff")
        self.InfoFrame.grid(row=1,column=0,sticky="ew",pady=(20,0), padx=20)
        
        customtkinter.CTkLabel(self.InfoFrame, text="Informations Client",font=customtkinter.CTkFont(size=13, weight="bold")).grid(row=0, column=0,sticky="w",padx=30, pady=(4,2))
        
        customtkinter.CTkFrame(self.InfoFrame, width=770, height=2, fg_color="lightgrey").grid(row=1,column=0, padx=0, pady=(2,10))
        
        self.nomComplet = customtkinter.CTkLabel(self.InfoFrame, text=f"{user.prenoms} {user.nom}", font=("Inter Bold",12))
        self.nomComplet. grid(row=2, column=0, sticky="w", padx=40, pady=0)
        
        self.infoVar = customtkinter.StringVar()
        self.info = customtkinter.CTkLabel(self.InfoFrame,text=f"{user.email} | {user.tel}" ,font=("Inter", 11)) #textvariable=self.infoVar
        self.info.grid(row=3,column=0, stick="w", padx=40, pady=(0,15))
        
        
        #Detail Livraison 
        
        self.livraisonFrame = customtkinter.CTkFrame(self.frameCommande, width=900,fg_color="#fff")
        self.livraisonFrame.grid(row=2,column=0,sticky="nsew",pady=(20,0), padx=20)
        
        customtkinter.CTkLabel(self.livraisonFrame, text="Détails de livraison").grid(row=0, column=0,sticky="w",padx=30, pady=(4,2))
        customtkinter.CTkFrame(self.livraisonFrame, width=770, height=2, fg_color="lightgrey").grid(row=1,column=0, padx=0, pady=(2,10),sticky="w")
        
            #Adresse
            
        customtkinter.CTkLabel(self.livraisonFrame, text="Adresse", font=("Inter Bold", 12)).grid(row=2, column=0,sticky="w",padx=30, pady=(7,0))
        
        self.adresseFrame = customtkinter.CTkFrame(self.livraisonFrame,fg_color="#fff",border_width=1,border_color="lightgrey",width=690)
        self.adresseFrame.grid(row=3, column=0, sticky="nsew", padx=40, pady=10)
        
        customtkinter.CTkLabel(self.adresseFrame, text="Ville").grid(row=0, column=0, sticky="w",pady=(20,0),padx=(60,40))
        
        self.entry_ville =customtkinter.CTkEntry(self.adresseFrame)
        self.entry_ville.grid(row=1, column=0, padx=(60,40), pady=(2,30), ipadx=20)
        # Initialiser un attribut pour suivre l'ID de l'événement précédent
        self.last_keypress = None

        
        
        customtkinter.CTkLabel(self.adresseFrame, text="Quartier").grid(row=0, column=1, sticky="w",pady=(20,0))
        
        self.entry_quartier = customtkinter.CTkEntry(self.adresseFrame)
        self.entry_quartier.grid(row=1, column=1,  padx=(0,40), pady=(2,30), ipadx=15)
        
        customtkinter.CTkLabel(self.adresseFrame, text="Rue,appartement").grid(row=0, column=2, sticky="w",pady=(20,0))
        
        self.entry_complement = customtkinter.CTkEntry(self.adresseFrame)
        self.entry_complement.grid(row=1, column=2,  padx=0, pady=(2,30),sticky="e",ipadx=20)
        
        
            #Mode de livraison
        
        customtkinter.CTkLabel(self.livraisonFrame, text="Mode de livraison", font=("Inter Bold", 12)).grid(row=4, column=0,sticky="w",padx=30, pady=(7,0))
        
        self.modeLivraison_var = tkinter.StringVar(value="")
        
        self.modeLivraisonFrame1 = customtkinter.CTkFrame(self.livraisonFrame, border_width=1, border_color="lightgrey", fg_color="#fff")
        self.modeLivraisonFrame1.grid(row=5, column=0,sticky="w", padx=40, pady=10)
        self.pointRelais = customtkinter.CTkRadioButton(master=self.modeLivraisonFrame1,text="Point relais", variable=self.modeLivraison_var, value="relais")
        self.pointRelais.grid(row=0, column=0, pady=10, padx=(20,0), sticky="w", ipadx=0)
        self.pointRelais.configure(state="disabled")
        
        customtkinter.CTkFrame(self.modeLivraisonFrame1, width=690, height=2, fg_color="lightgrey").grid(row=1,column=0, padx=0, pady=(0,10),sticky="w")
        customtkinter.CTkLabel(self.modeLivraisonFrame1,text="Veuillez sélectionner un point de relais SVP :",).grid(row=2,column=0,sticky="w",padx=20,pady=(0,5))
        
        self.point =customtkinter.CTkLabel(self.modeLivraisonFrame1,text="Désolé,nous ne disposons pas de points relais dans vôtre ville pour le moment",text_color="red",font=("Inter Bold", 10)) #.grid(row=0,column=0,sticky="e",padx=(5,100),pady=(5,5))
        
        self.selectRelais = customtkinter.CTkComboBox(self.modeLivraisonFrame1,height=35,
                                                    values=[' '])
        self.selectRelais.grid(row=2,column=0, padx=(0,70),sticky="e",pady=(0,25))
        self.selectRelais.configure(state="disabled")
        
        
        self.livraison, self.livraison_city = self.get_livraisons() #Récupérer les tarifs de livraion
        
        self.relaisPrix = customtkinter.IntVar()
        self.relaisPrixVar=customtkinter.StringVar(value="$")
        customtkinter.CTkLabel(self.modeLivraisonFrame1,textvariable=self.relaisPrixVar, font=("Inter Bold", 14),text_color="dark blue").grid(row=3,column=0, sticky="e", padx=30, pady=(0,5))
        
        
        
        self.modeLivraisonFrame2 = customtkinter.CTkFrame(self.livraisonFrame,border_width=1, border_color="lightgrey", fg_color="#fff")
        self.modeLivraisonFrame2.grid(row=6, column=0,sticky="w", padx=40, pady=10)
        self.aDomicile = customtkinter.CTkRadioButton(master=self.modeLivraisonFrame2,text="Livraison à domicile", variable=self.modeLivraison_var, value="domicile")
        self.aDomicile.grid(row=0, column=0, pady=(12,10), padx=20, sticky="w")
        
        self.domicilePrix = customtkinter.IntVar()
        self.domicilePrixVar=customtkinter.StringVar(value="$")
        customtkinter.CTkLabel(self.modeLivraisonFrame2,textvariable=self.domicilePrixVar, font=("Inter Bold", 14),text_color="dark blue").grid(row=1,column=0, sticky="e", padx=30, pady=(0,1))
        
        customtkinter.CTkFrame(self.modeLivraisonFrame2, width=690, height=1, fg_color="#fff").grid(row=2,column=0, padx=0, pady=(0,2),sticky="w")
        
        self.entry_ville.bind("<KeyRelease>", self.on_keyrelease_combined)
        self.selectRelais.bind("<<ComboboxSelected>>", self.update_livraison)
        self.selectRelais.bind("<FocusIn>", self.update_livraison)
        
        self.prix_liv=0 #Pour capturer le cout de la livraison
        self.modeLivraison_var.trace_add("write", self.prixLivraison) #Pour tracer les changement du bouton radio
        
        
        #List des produits
        
        
        customtkinter.CTkLabel(self.livraisonFrame, text="Produits du panier", font=("Inter Bold", 12)).grid(row=7, column=0,sticky="w",padx=30, pady=(7,0))
        customtkinter.CTkButton(self.livraisonFrame, text="Modifier mon panier", command=modifierPanier, fg_color="transparent",hover_color="dark blue",hover=False, border_width=0, font=("Arial", 13), text_color="blue").grid(row=7, column=0,sticky="e",padx=30, pady=(7,0))
        
        self.listProdFrame = customtkinter.CTkFrame(self.livraisonFrame,fg_color="#fff",border_width=1,border_color="lightgrey",width=690)
        self.listProdFrame.grid(row=8, column=0, sticky="nsew", padx=40, pady=10)
        
        self.produits = self.get_panier(user_id)
        
        self.listProduit(self.produits)

    
        
        #Recap Commande
        
            #Mode de paiement
            
        self.droiteFrame = customtkinter.CTkFrame(self.frameCommande, fg_color="transparent")
        self.droiteFrame.grid(row=1,column=1,rowspan=2, sticky="new", padx=5, pady=(20,0))
    
        # Variable pour suivre la sélection
        self.var = customtkinter.StringVar(value="")  # Option par défaut sélectionnée
        
        # Conteneur pour les boutons radio avec images
        self.boutModePFrame = customtkinter.CTkFrame(self.droiteFrame, fg_color="#fff")
        self.boutModePFrame.grid(row=1,column=1,sticky="ew", padx=5, pady=0)
        customtkinter.CTkLabel(self.boutModePFrame, text="Mode de paiement").grid(row=0, column=0,columnspan=3, sticky="w",padx=20, pady=(4,2))
       
        customtkinter.CTkFrame(self.boutModePFrame, width=260, height=2, fg_color="lightgrey").grid(row=1,column=0,columnspan=3, padx=0, pady=(2,10))
        
        # Chargement des images
        self.images = {
            "Carte Bancaire": self.load_image(relative_to_assets("visa2.png"),(30, 30)),
            "Wave": self.load_image(relative_to_assets("wave.jpg"),(30, 30)),
            "A la livraison": self.load_image(relative_to_assets("cashdelivery.png"),(30, 30))
        }
        
        # Paiement Visa
        
        self.modePaiementInfoFrame1 = customtkinter.CTkFrame(self.boutModePFrame, fg_color="#fff", border_width=1, border_color="blue")
        self.modePaiementInfoFrame1.grid(row=3, column=0, columnspan=3, sticky="nsew",pady=10, padx=6)
        
        customtkinter.CTkLabel(self.modePaiementInfoFrame1,text="Payer par carte", text_color="blue",font=customtkinter.CTkFont(size=13, weight="bold")).grid(row=0, column=0,columnspan=2, padx=5,pady=3, sticky="w")
        
        self.numeroCarte = customtkinter.CTkEntry(self.modePaiementInfoFrame1,placeholder_text="Numéro de la carte",width=190,border_color="blue", border_width=1)
        self.numeroCarte.grid(row=1,column=0,columnspan=2, padx=30)
        
        customtkinter.CTkLabel(self.modePaiementInfoFrame1,text="Date d'expiration", font=customtkinter.CTkFont(size=10),text_color="blue").grid(row=2, column=0,columnspan=2, padx=30,pady=0, sticky="e")
        
        self.moisCarte = customtkinter.CTkComboBox(self.modePaiementInfoFrame1, 
                                                  values=[f"{i:02}" for i in range(1, 13)],width=80,
                                                  border_color="blue", border_width=1)  
        self.moisCarte.grid(row=3, column=0, pady=(2,10),padx=(30,10), sticky="w")
        liste_annees = list(range(2024, 2055))
        self.anneeCarte = customtkinter.CTkComboBox(self.modePaiementInfoFrame1,
                                                  values=[str(annee).ljust(8) for annee in liste_annees],width=90,
                                                  border_color="blue", border_width=1)  
        self.anneeCarte.grid(row=3, column=1, pady=(2,10), padx=(0,15),sticky="w")

        self.cvvCarte = customtkinter.CTkEntry(self.modePaiementInfoFrame1, 
                             placeholder_text="CVV", 
                             width=40,  # Ajustez cette valeur si nécessaire
                             height=30,
                             validate="key",  # Cela permet de valider les entrées
                             validatecommand=(self.register(self.validate_cvv), "%P"),
                             border_color="blue", border_width=1) 
        self.cvvCarte.grid(row=4, column=0,padx=30, pady=10,sticky="w")

        
        
        # Paiement Wave
        
        self.modePaiementInfoFrame2 = customtkinter.CTkFrame(self.boutModePFrame, fg_color="#fff", border_width=1, border_color="lightblue")
        self.modePaiementInfoFrame2.grid(row=3, column=0, columnspan=3, sticky="nsew",pady=10, padx=6)
        
        customtkinter.CTkLabel(self.modePaiementInfoFrame2,text="Payer par Wave", text_color="lightblue",font=customtkinter.CTkFont(size=13, weight="bold")).grid(row=0, column=0, padx=5,pady=3, sticky="w")
        
        self.tel_frame = customtkinter.CTkFrame(self.modePaiementInfoFrame2, fg_color="#fff")  # Conteneur pour l'indicatif et le champ
        self.tel_frame.grid(row=1, column=0, pady=10, padx=10, sticky="ew")

        self.entry_indicatif = customtkinter.CTkEntry(self.tel_frame, width=10, placeholder_text="+225",border_color="lightblue", border_width=1)
        self.entry_indicatif.pack(side="left", padx=(0, 5), ipadx=20)  # Petite marge à droite

        
        self.numeroWave = customtkinter.CTkEntry(self.tel_frame,placeholder_text="Entrez le numéro", border_color="lightblue", border_width=1)
        self.numeroWave.pack(side="left", fill="x", expand=True,ipadx=25)
        
        # Paiment à la livraison
        
        self.modePaiementInfoFrame3 = customtkinter.CTkFrame(self.boutModePFrame, fg_color="#fff", border_width=1, border_color="orange")
        self.modePaiementInfoFrame3.grid(row=3, column=0, columnspan=3, sticky="nsew",pady=10, padx=10)
        
        customtkinter.CTkLabel(self.modePaiementInfoFrame3,text="Payer à la livraison", text_color="orange",font=customtkinter.CTkFont(size=13, weight="bold")).grid(row=0, column=0, padx=10,pady=3, sticky="w")
        
        customtkinter.CTkLabel(
            self.modePaiementInfoFrame3,
            text="Vous payerez la total en cash à la livraison",
            anchor="center",        
            wraplength=180,
            font=("Inter Bold",12)        
        ).grid(row=1, column=0, padx=(40,0), pady=(0,7), sticky="nsew")
        

        # Bouton de paiement
        self.image_buttons = {}
        for i, (key, img) in enumerate(self.images.items()):
            button = customtkinter.CTkButton(
                self.boutModePFrame,
                image=img,
                text="",  # Pas de texte, uniquement l'image
                fg_color="lightgray",  # Couleur par défaut
                hover_color="gray",    # Couleur au survol
                border_width=2,
                corner_radius=10,
                width=60,  # Largeur du bouton
                height=40, 
                command=lambda k=key: self.on_select(k)  # Passe la clé sélectionnée
            )
            button.grid(row=2, column=i, padx=10, pady=10)
            self.image_buttons[key] = button
            
        # Sélection initiale
        self.on_select()
        
        
        #Recap 
        
        self.recapFrame = customtkinter.CTkFrame(self.droiteFrame, fg_color="#fff")
        self.recapFrame.grid(row=2,column=1,sticky="ew", padx=5, pady=30)
        
        customtkinter.CTkLabel(self.recapFrame, text="Résumé de commande").grid(row=0, column=0, sticky="w",padx=20, pady=(4,2))
       
        customtkinter.CTkFrame(self.recapFrame, width=260, height=2, fg_color="lightgrey").grid(row=1,column=0, padx=0, pady=(2,10),sticky="ew")
        
        
        #Total produits
        
        n=len(self.produits)
        self.nbProd = customtkinter.StringVar(value=f"Total produit ({n})")
        self.prix_prod = self.prix_panier(self.produits)
        
        
        customtkinter.CTkLabel(self.recapFrame, textvariable=self.nbProd).grid(row=2, column=0, sticky="w",padx=10)
        
        self.coutPVar = customtkinter.StringVar(value=f"{self.prix_prod} FCFA")
        customtkinter.CTkLabel(self.recapFrame, textvariable=self.coutPVar).grid(row=2, column=0, sticky="e" ,padx=10)
        
            #Livraison
            
        
        customtkinter.CTkLabel(self.recapFrame, text="Frais de livraison").grid(row=3, column=0, sticky="w",padx=10)
        
        
        self.coutLivVar = customtkinter.StringVar(value=f"{self.prix_liv} FCFA")
        customtkinter.CTkLabel(self.recapFrame, textvariable=self.coutLivVar).grid(row=3, column=0, sticky="e",padx=10)
        
            #Total
        
        customtkinter.CTkLabel(self.recapFrame, text="Total à payer").grid(row=4, column=0, sticky="w",padx=10, pady=(20,15))
        self.Montant = self.prix_liv + self.prix_prod
        self.coutTotVar = customtkinter.StringVar(value=f"{self.Montant} FCFA")
        customtkinter.CTkLabel(self.recapFrame, textvariable=self.coutTotVar, font=customtkinter.CTkFont(size=16, weight="bold")).grid(row=4, column=0, sticky="e",padx=10,pady=(15,15))
        
        customtkinter.CTkFrame(self.recapFrame, width=260, height=2, fg_color="lightgrey").grid(row=5,column=0, padx=0, pady=(2,10),sticky="ew")
        
        self.boutonCommander = customtkinter.CTkButton(self.recapFrame,text="Confirmer la commande", anchor="center",corner_radius=5, command=self.valider)
        self.boutonCommander.grid(row=6, column=0,padx=15, pady=(0,20), sticky="ew")
        
    
        

        
    def load_image(self, path, size):
        """Charge et redimensionne une image."""
        img = Image.open(path).resize(size, Image.LANCZOS)
        return customtkinter.CTkImage(img, size=size) 

    def on_select(self, selected_option=None):
        # Masquer toutes les frames
        self.modePaiementInfoFrame1.grid_forget()
        self.modePaiementInfoFrame2.grid_forget()
        self.modePaiementInfoFrame3.grid_forget()
        
        # Changer la couleur des boutons pour refléter la sélection
        for key, button in self.image_buttons.items():
            if key == selected_option:
                button.configure(fg_color="blue")  # Couleur pour le bouton actif
            else:
                button.configure(fg_color="lightgray")  # Couleur pour les autres boutons
                
            self.selected_mode = None
            self.detail_paiement = None #pour stocker les infos de paiement

        
        if selected_option == "Carte Bancaire":
            self.modePaiementInfoFrame1.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10, padx=6)
            
            self.selected_mode = 1 #Clé du mode de paiement
            date_expiration = f"{self.moisCarte.get()}/{self.anneeCarte.get()}"
            
            import base64

            self.detail_paiement = {
                "nom_titulaire": f"{user.nom} {user.prenoms}",
                "montant": str(self.Montant),  # Convertir montant en chaîne pour JSON
                "no_carte": base64.b64encode(cipher_suite.encrypt(self.numeroCarte.get().encode('utf-8'))).decode('utf-8'),  # Encodage Base64
                "date_expiration": base64.b64encode(cipher_suite.encrypt(date_expiration.encode('utf-8'))).decode('utf-8'),  # Encodage Base64
                "cvv": base64.b64encode(cipher_suite.encrypt(self.cvvCarte.get().encode('utf-8'))).decode('utf-8')  # Encodage Base64
            }

    
        elif selected_option == "Wave":
            self.modePaiementInfoFrame2.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10, padx=6)
            self.selected_mode = 2
            numero = f"{self.entry_indicatif} {self.numeroWave}"
            import base64

            self.detail_paiement = {
                "nom_titulaire": f"{user.nom} {user.prenoms}",
                "montant": f"{self.Montant}",  # Garder le montant en entier si c'est un int attendu
                "no_wave": base64.b64encode(cipher_suite.encrypt(numero.encode('utf-8'))).decode('utf-8')  # Encodage Base64
            }

            
        elif selected_option == "A la livraison":
            self.modePaiementInfoFrame3.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10, padx=6)
            self.selected_mode = 3
            
            self.detail_paiement = {
            "nom_titulaire": f"{user.nom} {user.prenoms}" ,
            "montant": self.Montant,
        }
            
                
        
    def validate_cvv(self, new_value):
        # Limiter la longueur du texte à 3 caractères
        if len(new_value) > 3:
            return False
        # Vérifier que le texte ne contient que des chiffres
        return True
        
    def get_panier(self,id):
        try:
            query = "SELECT nom, nombre_article, prix , image, produit_id FROM panier INNER JOIN produit ON produit.id = produit_id WHERE panier.client_id = %s"
            cursor.execute(query,(id,))
            produits = cursor.fetchall()
            
            for i in produits: 
                print(i)
            return produits

        except mysql.connector.Error as err:
            print(f"Erreur : {err}")
            return []
        
    def prix_panier(self,produits):
        prix = 0
        for i in produits:
            prix = prix + i[2]*i[1]
            
        return prix


    def listProduit(self,produits):
        if not self.listProdFrame.winfo_exists():
            print("Erreur : Le cadre self.listProdFrame n'existe pas.")
            return
        
        for idx, produit in enumerate(produits):
            try:
                # Charger l'image si elle existe
                image_path = relative_to_assets(f"{produit[3]}")
                if os.path.exists(image_path):
                    imgi = customtkinter.CTkImage(light_image=Image.open(image_path), size=(50, 50))
                else:
                    print(f"Image non trouvée : {image_path}")
                    continue
                
                customtkinter.CTkLabel(
                    self.listProdFrame, text="", image=imgi
                ).grid(row=idx * 3, column=0, rowspan=2, padx=(20, 10), pady=10, sticky="wns")
                
                customtkinter.CTkLabel(
                    self.listProdFrame, text=f"{produit[0]}", font=customtkinter.CTkFont(size=11)
                ).grid(row=idx * 3, column=0, sticky="sw", pady=(10, 0), padx=(90, 0))
                
                customtkinter.CTkLabel(
                    self.listProdFrame, text=f"Quantité : {produit[1]}", font=customtkinter.CTkFont(size=10)
                ).grid(row=idx * 3 + 1, column=0, sticky="nw", pady=0, padx=(90, 0))
                
                customtkinter.CTkLabel(
                    self.listProdFrame, text=f"{produit[2]} FCFA (1)", font=customtkinter.CTkFont(size=13)
                ).grid(row=idx * 3 + 1, column=1, sticky="e", padx=(80, 0))

                customtkinter.CTkFrame(
                    self.listProdFrame, height=2, fg_color="lightgrey"
                ).grid(row=idx * 3 + 2, column=0, columnspan=2, padx=(20, 0), pady=(2, 10), sticky="ew")
            
            except Exception as e:
                print(f"Erreur lors de l'ajout du produit : {produit}. Détails : {e}")

    
        
    def get_villeQuartier(self):
        global longueur
        try:
            query = "SELECT city, quartier, FROM ville"
            cursor.execute(query)
            rows = cursor.fetchall()
            # Récupérer les colonnes
            columns = [desc[0] for desc in cursor.description]
            
            longueur = len(rows)
            print(rows[1])

            return columns, rows

        except mysql.connector.Error as err:
            print(f"Erreur : {err}")
            return [], []
        
    def on_keyrelease(self, event=None):
        """ Déclenché après chaque frappe, mais attend 500 ms avant de vérifier """
        # Annuler l'événement précédent si l'utilisateur tape trop vite
        if self.last_keypress is not None:
            self.entry_ville.after_cancel(self.last_keypress)

        # Lancer la vérification de la ville après 500 ms
        self.last_keypress = self.entry_ville.after(500, self.check_ville_existence)
        
    def on_keyrelease2(self, event=None):
        """ Déclenché après chaque frappe, mais attend 500 ms avant de vérifier """
        # Annuler l'événement précédent si l'utilisateur tape trop vite
        if self.last_keypress is not None:
            self.entry_ville.after_cancel(self.last_keypress)

        # Lancer la vérification de la ville après 500 ms
        self.last_keypress = self.entry_ville.after(500, self.update_livraison2)
        
    def on_keyrelease2(self, event=None):
        """ Déclenché après chaque frappe, mais attend 500 ms avant de vérifier """
        # Annuler l'événement précédent si l'utilisateur tape trop vite
        if self.last_keypress is not None:
            self.entry_ville.after_cancel(self.last_keypress)

        # Lancer la vérification de la ville après 500 ms
        self.last_keypress = self.entry_ville.after(500, self.update_livraison)

    def check_ville_existence(self):
        global city, quartiers
        """ Vérifier si la ville existe dans la base de données """
        ville_input = self.entry_ville.get()  # Récupérer la valeur entrée par l'utilisateur
        if not ville_input:
            return  # Si l'utilisateur n'a rien saisi, ne rien faire

        try:
            # Requête pour vérifier si la ville existe dans la base de données
            query = "SELECT city FROM ville WHERE city = %s"
            cursor.execute(query, (ville_input,))  # Exécuter la requête avec la ville comme paramètre
            results = cursor.fetchall()
            
            query = "SELECT quartier FROM ville WHERE city = %s"
            cursor.execute(query, (ville_input,))  # Exécuter la requête avec la ville comme paramètre
            results1 = cursor.fetchall()
            
            city = [list(result) for result in results]
            
            
            quartiers = [list(result1) for result1 in results1]
            
            quartiers = [item[0] for item in quartiers]
            print(quartiers)

            if results:
                # Si la ville existe dans la base de données
                print(f"La ville {ville_input} existe dans la base de données.")
                self.pointRelais.configure(state="normal")
                self.selectRelais.configure(state="normal")
                self.point.grid_forget()
                self.selectRelais.set(quartiers[0])
                self.selectRelais.configure(values=quartiers)
                print(self.prix_liv)
                self.modeLivraison_var.set(None)
                self.prix_liv=0
                self.coutLivVar.set(f"{self.prix_liv} FCFA")
                self.Montant = self.prix_liv + self.prix_prod
                self.coutTotVar.set(f"{self.Montant} FCFA")
                
            else:
                # Si la ville n'existe pas
                print(f"La ville {ville_input} n'existe pas dans la base de données.")
                print(self.domicilePrix.get())
                self.pointRelais.configure(state="disabled")
                self.selectRelais.configure(state="disabled")
                self.selectRelais.configure(values=[' '])
                self.selectRelais.set('')
                # if self.modeLivraison_var.get()==
                self.domicilePrix.set(7200)
                self.modeLivraison_var.set("domicile")
                
                self.prix_liv = self.domicilePrix.get()
                self.coutLivVar.set(f"{self.prix_liv} FCFA")
                self.Montant = self.prix_liv + self.prix_prod
                self.coutTotVar.set(f"{self.Montant} FCFA")
                self.point.grid(row=0,column=0,sticky="e",padx=(5,100),pady=(5,5))
        
                
        

        except mysql.connector.Error as e:
            # Gestion des erreurs de base de données
            print(f"Erreur lors de la vérification de la ville : {e}")
            
    def display_message(self, title, message):
        """ Afficher un message contextuel (comme une boîte de message) """
        messagebox.showinfo(title, message)  # Affichage d'un message contextuel avec info
        
        
    
    def ajouter_paiement_commande(self,commande_id, mode_paiement_id, montant, details_paiement):

        try:
            # Vérification si la commande existe
            cursor.execute("SELECT COUNT(*) FROM DetailCommande WHERE id = %s", (commande_id,))
            commande_exists = cursor.fetchone()[0]

            if commande_exists == 0:
                raise Exception("Commande non trouvée")

            # Insertion du paiement dans la table Paiement
            query = """
                INSERT INTO Paiement (commande_id, mode_paiement_id, montant, details_paiement)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (commande_id, mode_paiement_id, montant, json.dumps(details_paiement)))

            # Commit des modifications
            conn.commit()

            print("Paiement ajouté avec succès")

        except Exception as e:
            print(f"Erreur : {e}")
            conn.rollback()

            
    def get_livraisons(self):
            # Connexion à la base de données
        try:
            with conn.cursor() as cursor:
                # Requête SQL pour récupérer les quartiers et les prix de livraison
                query = "SELECT quartier, livraison FROM Ville"
                cursor.execute(query)

                # Récupérer les résultats sous forme de dictionnaire
                result = cursor.fetchall()
                quartiers_livraisons = {row[0].lower(): row[1] for row in result}
                
                # Requête SQL pour récupérer les qvilles et les prix de livraison
                query = "SELECT city, livraison FROM Ville"
                cursor.execute(query)

                # Récupérer les résultats sous forme de dictionnaire
                result = cursor.fetchall()
                city_livraisons = {row[0].lower(): row[1] for row in result}

                return quartiers_livraisons, city_livraisons
        finally:
            # Fermer la connexion à la base de données
            print("OK")
            
    def update_livraison(self,event=None):
        """Cette fonction est appelée lorsqu'un quartier est sélectionné."""
        # Récupérer le quartier sélectionné
        relais_selectionne = self.selectRelais.get().lower()

        # Obtenir le prix de livraison associé au quartier sélectionné
        prix_livraison = self.livraison.get(relais_selectionne, 6000)
        
        print(f"{relais_selectionne} Le prix est {prix_livraison}")
        self.relaisPrix.set(int(prix_livraison))
        # Mettre à jour la variable qui affiche le prix
        self.relaisPrixVar.set(f"{prix_livraison} FCFA")
        
        
        

    def update_livraison2(self,event=None):
        """Cette fonction est appelée lorsqu'un quartier est sélectionné."""
        # Récupérer le quartier sélectionné
        relais_selectionne = self.entry_ville.get().lower()

        # Obtenir le prix de livraison associé au quartier sélectionné
        prix = self.livraison_city.get(relais_selectionne, 6000)
        print(relais_selectionne, prix)
        # Mettre à jour la variable qui affiche le prix
        self.domicilePrix.set(int(prix)*1.2)
        self.domicilePrixVar.set(f"{prix*1.2} FCFA")

    def on_keyrelease_combined(self, event=None):
        """Déclenché après chaque frappe, exécute plusieurs actions après un délai."""
        # Annuler l'événement précédent si l'utilisateur tape trop vite
        if self.last_keypress is not None:
            self.entry_ville.after_cancel(self.last_keypress)

        # Lancer les vérifications et mises à jour après 500 ms
        self.last_keypress = self.entry_ville.after(500, self.execute_all_keyrelease_actions)

    def execute_all_keyrelease_actions(self):
        """Exécute toutes les actions nécessaires après un délai."""
        self.check_ville_existence()  # Action 1
        self.update_livraison2()      # Action 2
        self.update_livraison()       # Action 3
        
    def prixLivraison(self,*args):
        if self.modeLivraison_var.get() =="relais":
            self.prix_liv = self.relaisPrix.get()
            self.coutLivVar.set(f"{self.prix_liv} FCFA")
            self.Montant = self.prix_liv + self.prix_prod
            self.coutTotVar.set(f"{self.Montant} FCFA")
        else: 
            self.prix_liv = self.domicilePrix.get()
            self.coutLivVar.set(f"{self.prix_liv} FCFA")
            self.Montant = self.prix_liv + self.prix_prod
            self.coutTotVar.set(f"{self.Montant} FCFA")
            print(self.produits)
            
        
        
            
    def prix_panier(self,produits):
        self.prix = 0
        for i in produits:
            self.prix = self.prix + i[2]*i[1]
            
        return self.prix


        
    def validWave(self):
        if self.selected_mode == 2:
            # Vérifie si les champs sont remplis
            if self.entry_indicatif.get() != "" and self.numeroWave.get() != "":
                self.status = True  # Mettre à jour l'attribut de la classe
            else:
                self.status = False
        else:
            self.status = True  # Si le mode sélectionné n'est pas 2

    def validCarte(self):
        if self.selected_mode == 1:
            # Vérifie si tous les champs nécessaires sont remplis
            if (self.numeroCarte.get() != "" and self.cvvCarte.get() != "" and
                self.moisCarte.get() != "" and self.anneeCarte.get() != ""):
                self.status = True  # Mettre à jour l'attribut de la classe
            else:
                self.status = False
        else:
            self.status = True  # Si le mode sélectionné n'est pas 1

    def valider(self):
        # Appel des méthodes de validation
        self.validCarte()
        self.validWave()

        print(self.status, self.selected_mode)
        if self.entry_ville.get() != "" and self.entry_quartier.get() != "" and self.status != False:
            try:
                with conn.cursor() as cursor:
                    # Requête SQL pour ajouter les détails de la commande
                    query = "INSERT INTO DetailCommande (Ville_de_residence, commune, residence, montant_total) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (self.entry_ville.get(), self.entry_quartier.get(), self.entry_complement.get(), self.Montant))

                    # Commit des modifications
                    conn.commit()
                    
                    cle_commande = cursor.lastrowid  # Clé de la commande enregistrée
                    
                    # Requête SQL pour ajouter les produits dans la commande
                    if self.produits != []:
                        for produit in self.produits:
                            query = "INSERT INTO Commande (commande_id, client_id, produit_id, nombre_article) VALUES (%s, %s, %s, %s)"
                            cursor.execute(query, (cle_commande, user_id, int(produit[-1]), int(produit[1])))

                    # Commit des modifications
                    conn.commit()
                    
                    print(self.detail_paiement)
                    
                    # Ajout du paiement
                    self.ajouter_paiement_commande(cle_commande, int(self.selected_mode), self.Montant, self.detail_paiement)

                    # Suppression du panier
                    query = "DELETE FROM Panier WHERE client_id = %s"
                    cursor.execute(query, (user_id,))

                    # Commit des modifications
                    conn.commit()
                    messagebox.showinfo("Réuissit", "Votre commande a été enrgistrée avec succès !")
                    app.destroy()
                    call(["python", "Accueil.py"])
            finally:
                print("ok")
                
        else:
            messagebox.showwarning("Oups !", "Veuillez remplir tous les champs pour continuer")




if __name__ == "__main__":
    app = Commander()
    app.mainloop()
    
