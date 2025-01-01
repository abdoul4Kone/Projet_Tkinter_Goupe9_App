import random
from datetime import datetime, timedelta
from faker import Faker
import hashlib
import mysql.connector

# Initialisation de Faker
fake = Faker()

# Noms de famille ivoiriens courants
noms_ivoiriens = [
    'Kouamé', 'Koné', 'Kouassi', 'Koffi', 'Konan', 'Yao', 'N\'Guessan', 'Outtara',
    'Diabaté', 'Diallo', 'Bamba', 'Coulibaly', 'Traoré', 'Cissé', 'Diomandé',
    'Touré', 'Bakayoko', 'Drogba', 'Kalou', 'Gervinho', 'Aurier', 'Dindé',
    'Gbagbo', 'Bédié', 'Sangaré', 'Soro', 'Konaté', 'Sylla', 'Doumbia'
]

# Prénoms masculins ivoiriens
prenoms_masculins = [
    'Kouadio', 'Kouamé', 'Koffi', 'Konan', 'Yao', 'Mamadou', 'Ibrahim',
    'Seydou', 'Souleymane', 'Bakary', 'Lacina', 'Didier', 'Salomon',
    'Wilfried', 'Serge', 'Jean', 'Emmanuel', 'Christian', 'Francis',
    'Pascal', 'Arthur', 'César', 'Franck', 'Michel', 'Paul'
]

# Prénoms féminins ivoiriens
prenoms_feminins = [
    'Amenan', 'Aya', 'Adjoua', 'Akissi', 'Ahou', 'Affoué', 'N\'Dri',
    'Rokia', 'Aminata', 'Fatoumata', 'Mariam', 'Marie', 'Christine',
    'Sylvie', 'Patricia', 'Florence', 'Christelle', 'Sandrine', 'Linda',
    'Vanessa', 'Rachelle', 'Sarah', 'Estelle', 'Grâce', 'Béatrice'
]

def generer_date_naissance():
    """Génère une date de naissance pour un client entre 18 et 70 ans"""
    aujourd_hui = datetime.now()
    age = random.randint(18, 70)
    date = aujourd_hui - timedelta(days=age*365 + random.randint(0, 365))
    return date.strftime('%Y-%m-%d')

def generer_email(nom, prenom):
    """Génère un email basé sur le nom et prénom"""
    nom = nom.lower().replace("'", "").replace(" ", "")
    prenom = prenom.lower().replace("'", "").replace(" ", "")
    nombre = random.randint(1, 999)
    domaines = ['gmail.com', 'yahoo.fr', 'hotmail.com', 'outlook.com']
    return f"{prenom}.{nom}{nombre}@{random.choice(domaines)}"

def generer_numero_tel():
    """Génère un numéro de téléphone ivoirien"""
    prefixes = ['07', '01', '05']
    return f"+225{random.choice(prefixes)}{random.randint(10000000, 99999999)}"

def generer_mdp():
    """Génère un mot de passe hashé"""
    mdp_clair = fake.password(length=12)
    return hashlib.sha256(mdp_clair.encode()).hexdigest()

try:
    # Connexion à la base de données
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='e_commerce'
    )
    cursor = connection.cursor()

    # Génération et insertion des clients
    emails_utilises = set()
    
    for _ in range(200):
        sexe = random.choice(['Masculin', 'Feminin'])
        nom = random.choice(noms_ivoiriens)
        prenom = random.choice(prenoms_masculins if sexe == 'Masculin' else prenoms_feminins)
        
        # Génération d'un email unique
        email = generer_email(nom, prenom)
        while email in emails_utilises:
            email = generer_email(nom, prenom)
        emails_utilises.add(email)
        
        # Préparation des données du client
        client_data = (
            nom,
            prenom,
            sexe,
            generer_date_naissance(),
            email,
            generer_mdp(),
            generer_numero_tel()
        )
        
        # Requête SQL avec paramètres pour éviter les injections SQL
        requete = """
        INSERT INTO Client (nom, prenoms, sexe, date_naissance, email, mdp, numero_tel)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        # Exécution de la requête
        cursor.execute(requete, client_data)
    
    # Validation des insertions
    connection.commit()
    print(f"200 clients ont été insérés avec succès dans la base de données.")

except mysql.connector.Error as erreur:
    print(f"Erreur lors de l'opération sur la base de données: {erreur}")

finally:
    # Fermeture des ressources
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()
        print("Connexion à la base de données fermée.")