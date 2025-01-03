# session_manager.py
import mysql.connector
from tkinter import messagebox
import json
import os
import hashlib

class User:
    def __init__(self, id=None, nom=None, prenoms=None, email=None,numero_tel=None):
        self.id = id
        self.nom = nom
        self.prenoms = prenoms
        self.email = email
        self.numero_tel = numero_tel
    
    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'prenoms': self.prenoms,
            'email': self.email,
            'tel' : self.numero_tel
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(**data) if data else None

class SessionManager:
    _instance = None
    SESSION_FILE = "session.json"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SessionManager, cls).__new__(cls)
            cls._instance.user = None
            cls._instance.is_authenticated = False
            cls._instance.connect_to_database()
            cls._instance.load_session()
        return cls._instance
    
    def connect_to_database(self):
        try:
            self.db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="e_commerce"
            )
            self.cursor = self.db.cursor(buffered=True)
        except mysql.connector.Error as e:
            print(f"Erreur de connexion: {e}")
    
    def save_session(self):
        session_data = {
            'is_authenticated': self.is_authenticated,
            'user': self.user.to_dict() if self.user else None
        }
        try:
            with open(self.SESSION_FILE, 'w') as f:
                json.dump(session_data, f)
            print("Session sauvegardée")  # Debug
        except Exception as e:
            print(f"Erreur sauvegarde session: {e}")  # Debug
    
    def load_session(self):
        try:
            if os.path.exists(self.SESSION_FILE):
                with open(self.SESSION_FILE, 'r') as f:
                    data = json.load(f)
                    self.is_authenticated = data.get('is_authenticated', False)
                    user_data = data.get('user')
                    self.user = User.from_dict(user_data) if user_data else None
                print(f"Session chargée: {self.get_user_display_name()}")  # Debug
        except Exception as e:
            print(f"Erreur chargement session: {e}")  # Debug
    
    def login(self, email, password):
        try:
            if not hasattr(self, 'db') or not self.db.is_connected():
                self.connect_to_database()
                
            # Hachage du mot de passe saisi
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            
            
            query = "SELECT id, nom, prenoms, email , numero_tel FROM Client WHERE email = %s AND mdp = %s"
            self.cursor.execute(query, (email, hashed_password))
            result = self.cursor.fetchone()
            
            if result:
                self.user = User(
                    id=result[0],
                    nom=result[1],
                    prenoms=result[2],
                    email=result[3],
                    numero_tel=result[4]
                )
                self.is_authenticated = True
                self.save_session()
                print(f"Connexion réussie: {self.user.prenoms} {self.user.nom}")  # Debug
                return True
            return False
            
        except mysql.connector.Error as e:
            print(f"Erreur MySQL: {e}")  # Debug
            return False
    
    def logout(self):
        self.user = None
        self.is_authenticated = False
        if os.path.exists(self.SESSION_FILE):
            os.remove(self.SESSION_FILE)
    
    def get_user_display_name(self):
        if self.is_authenticated and self.user:
            
            return f"{self.user.prenoms} {self.user.nom}"
        return "Se connecter"
    
    def check_auth(self):
        if not self.is_authenticated:
            from subprocess import call
            call(["python", "Login.py"])
            return False
        return True
    
import json

# Chemin vers le fichier JSON
fichier_session = "session.json"

user_id = None
try:
    # Lire le fichier JSON
    with open(fichier_session, 'r') as fichier:
        session_data = json.load(fichier)

    # Vérifier si l'utilisateur est authentifié
    is_authenticated = session_data.get('is_authenticated', False)

    if is_authenticated:
        # Récupérer les données utilisateur
        user_data = session_data.get('user', {})
        user_id = user_data.get('id')  # Récupérer la clé "id"
        print(f"Utilisateur authentifié, ID: {user_id}")
    else:
        user_id=None
        print("L'utilisateur n'est pas authentifié.")

except FileNotFoundError:
    print(f"Le fichier {fichier_session} n'existe pas.")
except json.JSONDecodeError as e:
    print(f"Erreur lors du chargement du fichier JSON : {e}")
