import mysql.connector
from tkinter import messagebox
import pandas as pd

# Connect to MySQL database
def connect_to_database():
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
        
        
# Fonction pour insérer des données dans la table client
def ajouter_client():
    nom = entry_nom.get()
    prenom = entry_prenom.get()
    email = entry_email.get()
    mdp = entry_password.get()
    tel = entry_indicatif.get() + entry_tel.get() 
    birth_date = entry_birth.get()
    sexe = "H"
    
    

    if nom and prenom and email and mdp and tel and birth_date and sexe:  # Vérification si tous les champs sont remplis
        try:
            query = "INSERT INTO client (nom, prenoms,sexe,date_naissance,email,mdp,numero_tel) VALUES (%s, %s,%s, %s,%s, %s,%s)"
            values = (nom, prenom,sexe,birth_date,email,mdp,tel)
            cursor.execute(query, values)
            conn.commit()
            messagebox.showinfo("Succès", "Compte créer avec succès !")
            
        except mysql.connector.Error as err:
            messagebox.showerror("Erreur d'insertion", f"Erreur : {err}")
    else:
        messagebox.showwarning("Champs vides", "Veuillez remplir tous les champs !")
        
pays = [
    "Afghanistan", "Afrique du Sud", "Algérie", "Angola", "Argentine", "Australie", "Autriche", "Belgique", "Bénin", "Bolivie",
    "Brésil", "Burkina Faso", "Burundi", "Cambodge", "Cameroun", "Canada", "Chili", "Chine", "Colombie", "Comores", "Congo",
    "Côte d'Ivoire", "Croatie", "Danemark", "Égypte", "Espagne", "États-Unis", "Éthiopie", "Fidji", "Finlande", "France",
    "Gabon", "Gambie", "Ghana", "Grèce", "Guatemala", "Guinée", "Guinée-Bissau", "Haïti", "Honduras", "Hongrie", "Inde",
    "Indonésie", "Irak", "Iran", "Irlande", "Islande", "Israël", "Italie", "Japon", "Jordanie", "Kenya", "Koweït", "Laos",
    "Lesotho", "Liban", "Liberia", "Libye", "Liechtenstein", "Lituanie", "Luxembourg", "Madagascar", "Malaisie", "Malawi",
    "Maldives", "Mali", "Malte", "Maroc", "Maurice", "Mauritanie", "Mexique", "Moldavie", "Monaco", "Mongolie", "Mozambique",
    "Namibie", "Népal", "Nicaragua", "Niger", "Nigeria", "Norvège", "Nouvelle-Zélande", "Oman", "Ouganda", "Pakistan", "Palestine",
    "Panama", "Papouasie-Nouvelle-Guinée", "Paraguay", "Pays-Bas", "Pérou", "Philippines", "Pologne", "Portugal", "République Démocratique du Congo",
    "République Tchèque", "Roumanie", "Rwanda", "Saint-Kitts-et-Nevis", "Saint-Marin", "Saint-Vincent-et-les-Grenadines",
    "Salvador", "Samoa", "São Tomé-et-Príncipe", "Sénégal", "Serbie", "Seychelles", "Sierra Leone", "Singapour", "Slovaquie",
    "Slovénie", "Somalie", "Soudan", "Sri Lanka", "Suisse", "Suriname", "Swaziland", "Syrie", "Tanzanie", "Togo", "Trinité-et-Tobago",
    "Tunisie", "Turquie", "Ukraine", "Uruguay", "Vanuatu", "Venezuela", "Vietnam", "Yémen", "Zambie", "Zimbabwe"
]





indicatifs = [
    "+93", "+27", "+213", "+244", "+54", "+61", "+43", "+32", "+229", "+591",
    "+55", "+226", "+257", "+855", "+237", "+1", "+56", "+86", "+57", "+269",
    "+242", "+225", "+385", "+45", "+20", "+34", "+1", "+251", "+679", "+358",
    "+33", "+241", "+220", "+233", "+30", "+502", "+224", "+245", "+509", "+504",
    "+36", "+91", "+62", "+964", "+98", "+353", "+354", "+972", "+39", "+81",
    "+962", "+254", "+965", "+856", "+266", "+961", "+231", "+218", "+423", "+370",
    "+352", "+261", "+60", "+265", "+960", "+223", "+356", "+212", "+230", "+222",
    "+52", "+373", "+377", "+976", "+258", "+264", "+977", "+505", "+227", "+234",
    "+47", "+64", "+968", "+256", "+92", "+970", "+507", "+675", "+595", "+31",
    "+51", "+63", "+48", "+351", "+243", "+420", "+40", "+250", "+1869", "+378",
    "+1784", "+503", "+684", "+239", "+221", "+381", "+248", "+232", "+65", "+421",
    "+386", "+252", "+249", "+94", "+41", "+597", "+268", "+963", "+255", "+228",
    "+1868", "+216", "+90", "+380", "+598", "+678", "+58", "+84", "+967", "+260", "+263"
]




longueurs = [
    9, 10, 9, 9, 10, 9, 10, 9, 8, 8, 11, 8, 8, 9, 9, 10, 9, 9, 9, 9, 9, 10, 
    9, 8, 9, 9, 10, 9, 9, 9, 9, 9, 8, 9, 10, 8, 9, 9, 9, 8, 9, 10, 9, 9, 
    9, 9, 8, 9, 9, 9, 9, 9, 8, 9, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
    9, 8, 9, 8, 9, 10, 9, 9, 8, 9, 9, 9, 9, 9, 9, 8, 9, 8, 9, 9, 9, 9, 
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 
    9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 8, 9, 9, 9, 9, 9, 9, 9, 9, 9
]

data={
    'pays':pays,
    'indicatif' : indicatifs,
    'longueur': longueurs
}

df = pd.DataFrame(data)
df = df.sort_values(by="indicatif") 

def indicatifPays():
    return df["indicatif"].tolist()


# Dictionnaire des pays et indicatifs téléphoniques
pays_indicatifs = {
    "Afghanistan": "+93",
    "Afrique du Sud": "+27",
    "Algérie": "+213",
    "Angola": "+244",
    "Argentine": "+54",
    "Australie": "+61",
    "Autriche": "+43",
    "Belgique": "+32",
    "Bénin": "+229",
    "Bolivie": "+591",
    "Brésil": "+55",
    "Burkina Faso": "+226",
    "Burundi": "+257",
    "Cambodge": "+855",
    "Cameroun": "+237",
    "Canada": "+1",
    "Chili": "+56",
    "Chine": "+86",
    "Colombie": "+57",
    "Comores": "+269",
    "Congo": "+242",
    "Côte d'Ivoire": "+225",
    "Croatie": "+385",
    "Danemark": "+45",
    "Égypte": "+20",
    "Espagne": "+34",
    "États-Unis": "+1",
    "Éthiopie": "+251",
    "Fidji": "+679",
    "Finlande": "+358",
    "France": "+33",
    "Gabon": "+241",
    "Gambie": "+220",
    "Ghana": "+233",
    "Grèce": "+30",
    "Guatemala": "+502",
    "Guinée": "+224",
    "Guinée-Bissau": "+245",
    "Haïti": "+509",
    "Honduras": "+504",
    "Hongrie": "+36",
    "Inde": "+91",
    "Indonésie": "+62",
    "Irak": "+964",
    "Iran": "+98",
    "Irlande": "+353",
    "Islande": "+354",
    "Israël": "+972",
    "Italie": "+39",
    "Japon": "+81",
    "Jordanie": "+962",
    "Kenya": "+254",
    "Koweït": "+965",
    "Laos": "+856",
    "Lesotho": "+266",
    "Liban": "+961",
    "Liberia": "+231",
    "Libye": "+218",
    "Liechtenstein": "+423",
    "Lituanie": "+370",
    "Luxembourg": "+352",
    "Madagascar": "+261",
    "Malaisie": "+60",
    "Malawi": "+265",
    "Maldives": "+960",
    "Mali": "+223",
    "Malte": "+356",
    "Maroc": "+212",
    "Maurice": "+230",
    "Mauritanie": "+222",
    "Mexique": "+52",
    "Moldavie": "+373",
    "Monaco": "+377",
    "Mongolie": "+976",
    "Mozambique": "+258",
    "Namibie": "+264",
    "Népal": "+977",
    "Nicaragua": "+505",
    "Niger": "+227",
    "Nigeria": "+234",
    "Norvège": "+47",
    "Nouvelle-Zélande": "+64",
    "Oman": "+968",
    "Ouganda": "+256",
    "Pakistan": "+92",
    "Palestine": "+970",
    "Panama": "+507",
    "Papouasie-Nouvelle-Guinée": "+675",
    "Paraguay": "+595",
    "Pays-Bas": "+31",
    "Pérou": "+51",
    "Philippines": "+63",
    "Pologne": "+48",
    "Portugal": "+351",
    "République Démocratique du Congo": "+243",
    "République Tchèque": "+420",
    "Roumanie": "+40",
    "Rwanda": "+250",
    "Saint-Kitts-et-Nevis": "+1869",
    "Saint-Marin": "+378",
    "Saint-Vincent-et-les-Grenadines": "+1784",
    "Salvador": "+503",
    "Samoa": "+684",
    "São Tomé-et-Príncipe": "+239",
    "Sénégal": "+221",
    "Serbie": "+381",
    "Seychelles": "+248",
    "Sierra Leone": "+232",
    "Singapour": "+65",
    "Slovaquie": "+421",
    "Slovénie": "+386",
    "Somalie": "+252",
    "Soudan": "+249",
    "Sri Lanka": "+94",
    "Suisse": "+41",
    "Suriname": "+597",
    "Swaziland": "+268",
    "Syrie": "+963",
    "Tanzanie": "+255",
    "Togo": "+228",
    "Trinité-et-Tobago": "+1868",
    "Tunisie": "+216",
    "Turquie": "+90",
    "Ukraine": "+380",
    "Uruguay": "+598",
    "Vanuatu": "+678",
    "Venezuela": "+58",
    "Vietnam": "+84",
    "Yémen": "+967",
    "Zambie": "+260",
    "Zimbabwe": "+263"
}

def afficher_indicatif(event):
    pays_selectionne = combobox.get()
    indicatif = pays_indicatifs.get(pays_selectionne, "Indisponible")
    label_indicatif.config(text=f"Indicatif : {indicatif}")
        
        
def connect_to_database():
    'Cette fonction permet de se connecter à la base de donnée'
    import mysql.connector
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
        
def fillPanier(id_produit, nb):
    connect_to_database()
    from session_manager import user_id  # Charger l'ID de l'utilisateur connecté
    nb = int(nb)  # S'assurer que `nb` est un entier

    try:
        if nb > 0:
            # Ajouter ou mettre à jour le panier
            query = """
            INSERT INTO panier (client_id, produit_id, nombre_article)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE nombre_article = %s
            """
            cursor.execute(query, (user_id, id_produit, nb, nb))
        else:
            # Supprimer l'enregistrement si `nb` <= 0
            query = "DELETE FROM panier WHERE client_id = %s AND produit_id = %s"
            cursor.execute(query, (user_id, id_produit))

        # Valider la transaction
        conn.commit()
    except mysql.connector.Error as err:
        # Afficher une erreur en cas de problème avec la base de données
        messagebox.showerror("Erreur", f"Erreur de base de données : {err}")
        
# def update_nb(id_produit,nb):
#     from session_manager import user_id 
#     try:
#         if nb > 0:
#             # Ajouter ou mettre à jour le panier
#             query = """
#             INSERT INTO panier (client_id, produit_id, nombre_article)
#             VALUES (%s, %s, %s)
#             ON DUPLICATE KEY UPDATE nombre_article = %s
#             """
#             cursor.execute(query, (user_id, id_produit, nb, nb))
#         else:
#             # Supprimer l'enregistrement si `nb` <= 0
#             query = "DELETE FROM panier WHERE client_id = %s AND produit_id = %s"
#             cursor.execute(query, (user_id, id_produit))

#         # Valider la transaction
#         conn.commit()
#     except mysql.connector.Error as err:
#         # Afficher une erreur en cas de problème avec la base de données
#         messagebox.showerror("Erreur", f"Erreur de base de données : {err}")


        
