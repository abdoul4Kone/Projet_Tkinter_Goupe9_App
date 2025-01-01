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
from subprocess import call


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
#Retour à l'acccueil      
def home(): 
    app.destroy()
    call(["python", "Accueil.py"])
        
get_data(user_id)
customtkinter.set_appearance_mode("Light")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class Panier(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # configure window
        self.title("Commander")
        self.geometry("1100x580")
        # Désactiver le redimensionnement si nécessaire
        self.resizable(False, False)
        
        self.setup_ui()

        # configure grid layout (4x4)
        # self.grid_columnconfigure(1, weight=1)
        # self.grid_columnconfigure((2, 3), weight=0)
        # self.grid_rowconfigure((0, 1, 2), weight=1)
        
    def setup_ui(self):
        self.grid_columnconfigure((0,1), weight=2)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        
        # Modifiez cette ligne
        self.entete = customtkinter.CTkFrame(
            self,
            fg_color="#fff",
            corner_radius=0,
            height=60  # Retirez le int()
        )
        self.entete.grid(row=0, column=0, columnspan=2, padx=0, pady=0, sticky="nsew")
        self.entete.grid(row=0, column=0,columnspan=2, padx=0, pady=0,sticky="nsew")
        
        customtkinter.CTkButton(self.entete,width=100,text=" ",corner_radius=0,fg_color="transparent", hover=False, command=home,image= customtkinter.CTkImage(light_image=Image.open(relative_to_assets('logo.png')), size=(70, 50))).grid(row=0,column=0, sticky="nsw", padx=40)
        customtkinter.CTkLabel(self.entete, text="Mon panier", font=customtkinter.CTkFont(size=18, weight="bold"),text_color="#1B6392").grid(row=0,column=1, sticky="e", padx=(640,5))
        customtkinter.CTkButton(self.entete,width=40, text=" ",fg_color="#1B6392", hover=False, image= customtkinter.CTkImage(light_image=Image.open(relative_to_assets('cart.png')), size=(30, 30))).grid(row=0,column=2, sticky="e", padx=(0,40))

        self.frameCommande = customtkinter.CTkScrollableFrame(self,corner_radius=0,fg_color="lightgrey",scrollbar_button_color="lightgrey")
        self.frameCommande.grid(row=1, column=0,columnspan=2, padx=0, pady=(0,10),sticky="nsew")
        
        
        
        #Detail Livraison 
        
        self.livraisonFrame = customtkinter.CTkFrame(self.frameCommande, width=900,fg_color="#fff")
        self.livraisonFrame.grid(row=2,column=0,sticky="nsew",pady=(20,0), padx=20)
        
        customtkinter.CTkLabel(self.livraisonFrame, text="Détails de livraison").grid(row=0, column=0,sticky="w",padx=30, pady=(4,2))
        customtkinter.CTkFrame(self.livraisonFrame, width=770, height=2, fg_color="lightgrey").grid(row=1,column=0, padx=0, pady=(2,10),sticky="w")
        
        #List des produits
        
        
        customtkinter.CTkLabel(self.livraisonFrame, text="Produits du panier", font=("Inter Bold", 12)).grid(row=7, column=0,sticky="w",padx=30, pady=(7,0))
        
        self.listProdFrame = customtkinter.CTkFrame(self.livraisonFrame,fg_color="#fff",border_width=1,border_color="lightgrey",width=690)
        self.listProdFrame.grid(row=8, column=0, sticky="nsew", padx=40, pady=10)
        
        self.produits = self.get_panier(user_id)
        
        self.list = self.listProduit(self.produits)

        
            
        self.droiteFrame = customtkinter.CTkFrame(self.frameCommande, fg_color="transparent")
        self.droiteFrame.grid(row=1,column=1,rowspan=2, sticky="new", padx=5, pady=(20,0))
    
                #Recap 
        
        self.recapFrame = customtkinter.CTkFrame(self.droiteFrame, fg_color="#fff")
        self.recapFrame.grid(row=0,column=1,sticky="ew", padx=5, pady=0)
        
        customtkinter.CTkLabel(self.recapFrame, text="Résumé de commande").grid(row=0, column=0, sticky="w",padx=20, pady=(4,2))
       
        customtkinter.CTkFrame(self.recapFrame, width=260, height=2, fg_color="lightgrey").grid(row=1,column=0, padx=0, pady=(2,10),sticky="ew")
        
        
        #Total produits
        

        #Total produits
       
        self.n = len(self.produits)#Nombre de produits
        self.prix = self.prix_panier(self.produits)
        self.nbProd = customtkinter.StringVar(value=f"Total panier ({self.n})")
                
                
                    #Total
                
        customtkinter.CTkLabel(self.recapFrame, textvariable=self.nbProd).grid(row=3, column=0, sticky="w",padx=10, pady=(20,15))
                
        self.coutTotVar = customtkinter.StringVar(value=f"{self.prix} FCFA")
        customtkinter.CTkLabel(self.recapFrame, textvariable=self.coutTotVar, font=customtkinter.CTkFont(size=13, weight="bold"), text_color="#1B6392").grid(row=3, column=0, sticky="es",padx=10,pady=(15,15))
                
        customtkinter.CTkFrame(self.recapFrame, width=260, height=2, fg_color="lightgrey").grid(row=4,column=0, padx=0, pady=(2,10),sticky="ew")
                
        boutonCommander = customtkinter.CTkButton(self.recapFrame, command=self.commander, text="Commander", anchor="center",corner_radius=5, font=customtkinter.CTkFont(weight="bold"))
        boutonCommander.grid(row=5, column=0,padx=20, pady=(0,20), sticky="ew", ipady=5)

        
    
        

        
    def load_image(self, path, size):
        """Charge et redimensionne une image."""
        img = Image.open(path).resize(size, Image.LANCZOS)
        return customtkinter.CTkImage(img, size=size) 

        
    def get_panier(self, id):
            try:
                query = """
                    SELECT nom, nombre_article, prix, image, stock, produit_id 
                    FROM panier 
                    INNER JOIN produit ON produit.id = produit_id 
                    WHERE panier.client_id = %s
                """
                cursor.execute(query, (id,))
                produits = cursor.fetchall()

                # Convertir chaque tuple en liste
                produits = [list(produit) for produit in produits]

                for i in produits: 
                    print(i)  # Chaque ligne sera maintenant une liste
                return produits

            except mysql.connector.Error as err:
                print(f"Erreur : {err}")
                return []

    def prix_panier(self,produits):
        self.prix = 0
        for i in produits:
            self.prix = self.prix + i[2]*i[1]
            
        return self.prix


    import os

    def listProduit(self, produits):
        
        if self.produits == []:
            customtkinter.CTkLabel(self.listProdFrame, text="Votre panier est vide ! \nAjoutez des produits ",font=customtkinter.CTkFont(size=16), text_color="red").grid(row=0, column=0, sticky="nesw", padx=(250,0), ipady=20)
        if not self.listProdFrame.winfo_exists():
            print("Erreur : Le cadre self.listProdFrame n'existe pas.")
            return

        trash_img = self.load_image(relative_to_assets("trash.png"), (10, 10))

        for idx, produit in enumerate(produits):
            try:
                # Charger l'image si elle existe
                image_path = relative_to_assets(f"{produit[3]}")
                if os.path.exists(image_path):
                    imgi = customtkinter.CTkImage(light_image=Image.open(image_path), size=(50, 50))
                else:
                    print(f"Image non trouvée : {image_path}")
                    continue

                # Affichage de l'image
                customtkinter.CTkLabel(
                    self.listProdFrame, text="", image=imgi
                ).grid(row=idx * 4, column=0, rowspan=2, padx=(10, 5), pady=10, sticky="w")

                # Affichage du nom du produit
                customtkinter.CTkLabel(
                    self.listProdFrame, text=f"{produit[0]}", font=customtkinter.CTkFont(size=11)
                ).grid(row=idx * 4, column=1, sticky="w", pady=(10, 0), padx=(10, 5))

                # Affichage de la quantité
                quantity_label = customtkinter.CTkLabel(
                    self.listProdFrame, text=f"Quantité : {produit[1]}", font=customtkinter.CTkFont(size=10)
                )
                quantity_label.grid(row=idx * 4 + 1, column=1, sticky="w", pady=0, padx=(10, 5))

                from script import fillPanier
                # Boutons pour gérer la quantité
                def increase_quantity(x):
                    if produits[x][1] < produit[4]:  # Vérifie si la quantité est inférieure au stock maximum
                        produits[x][1] += 1  # Incrémentation de la quantité
                        quantity_label.configure(text=f"Quantité : {produits[x][1]}")  # Mise à jour du label
                        fillPanier(produits[x][-1], produits[x][1])  # Mise à jour du panier

                def decrease_quantity(x):
                    if produits[x][1] > 1:  # Vérifie si la quantité est supérieure à 1
                        produits[x][1] -= 1  # Décrémentation de la quantité
                        quantity_label.configure(text=f"Quantité : {produits[x][1]}")  # Mise à jour du label
                        fillPanier(produits[x][-1], produits[x][1])  # Mise à jour du panier

                def remove_product(x):
                    if messagebox.askyesno("Supprimer", "Supprimer cet article du panier ?") == True:
                        print(f"Suppression du produit : {produit[0]}")
                        
                        # Supprimer le produit de la base de données
                        try:
                            query = "DELETE FROM panier WHERE produit_id = %s AND client_id = %s"
                            cursor.execute(query, (produits[x][-1], user_id))
                            conn.commit()
                        except mysql.connector.Error as e:
                            messagebox.showerror("Erreur", f"Erreur de suppression dans la base de données : {e}")
                        
                        # Supprimer le produit de la liste locale
                        produits.pop(x)
                        print(x)
                        print(produits)
                        
                        # Rafraîchir la vue (effacer l'ancien contenu)
                        for widget in self.listProdFrame.winfo_children():
                            widget.destroy()
                        
                        # Redessiner la liste mise à jour
                        self.list = self.listProduit(produits)
                        

                        # Mettre à jour les variables d'affichage du panier
                        self.nbProd.set(f"Total panier ({len(produits)})")
                        self.coutTotVar.set(f"{self.prix_panier(produits)} FCFA")
                        
                     
                # Création des boutons
                customtkinter.CTkButton(
                    self.listProdFrame, text="+",  command=lambda idx=idx:increase_quantity(idx), width=30, height=20
                ).grid(row=idx * 4, column=3, sticky="ne", padx=(0, 10), pady=4)

                customtkinter.CTkButton(
                    self.listProdFrame, text="-",  command=lambda idx=idx:decrease_quantity(idx), width=30, height=20
                ).grid(row=idx * 4, column=4, sticky="nw", padx=0, pady=4)

                customtkinter.CTkButton(
                    self.listProdFrame, image=trash_img, text="", command=lambda idx=idx: remove_product(idx), width=30, height=20
                ).grid(row=idx * 4, column=4, sticky="ne", padx=(0, 10), pady=4)

                # Affichage du self.prix
                customtkinter.CTkLabel(
                    self.listProdFrame, text=f"{produit[2]} FCFA (1)", font=customtkinter.CTkFont(size=13)
                ).grid(row=idx * 4 + 1, column=4, sticky="e", padx=(10, 0))

                # Ligne de séparation
                customtkinter.CTkFrame(
                    self.listProdFrame, height=2, fg_color="lightgrey", width=640
                ).grid(row=idx * 4 + 2, column=0, columnspan=5, padx=(20, 0), pady=(2, 10), sticky="ew")

            except Exception as e:
                print(f"Erreur lors de l'ajout du produit : {produit}. Détails : {e}")

    
    def commander(self):
        if self.produits==[]:
            messagebox.showwarning("Oups!", "Votre panier est vide, veuillez ajoutez des produits pour commander")
        else:
            app.destroy()
            call(["python", "Commande.py"])
    




if __name__ == "__main__":
    app = Panier()
    app.mainloop()
    
    
