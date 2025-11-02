from flask import Flask, render_template, request, jsonify, redirect, url_for, session, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message
from datetime import datetime, timedelta
import os
import smtplib
import glob
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from urllib.parse import quote
from functools import wraps
from dotenv import load_dotenv
from supabase import create_client, Client

# Charger les variables d'environnement
load_dotenv()

# Crée l'application Flask
app = Flask(__name__)

# Clé secrète pour les sessions (changez cette valeur !)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'votre-cle-secrete-tres-longue-et-complexe-2024')

# Mot de passe admin (changez cette valeur !)
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'AdminConseilux2024!')

# Configuration de la base de données
# Utiliser un chemin absolu pour la base de données en production
if os.environ.get('VERCEL'):
    # En production Vercel, utiliser une base de données temporaire
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
else:
    # En développement local
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletter.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configuration Flask-Mail
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', '587'))
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL', 'False').lower() == 'true'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'contact@conseiluxtraining.com')

# Initialiser Flask-Mail et SQLAlchemy
mail = Mail(app)
db = SQLAlchemy(app)

# Initialiser Supabase
SUPABASE_URL = os.environ.get('SUPABASE_URL')
SUPABASE_KEY = os.environ.get('SUPABASE_KEY')
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✓ Supabase connecté avec succès")
    except Exception as e:
        print(f"⚠ Erreur de connexion à Supabase: {e}")
else:
    print("⚠ Variables Supabase non configurées - les avis utiliseront SQLite")

# ========== SYSTÈME DE CACHE SIMPLE ==========
# Cache en mémoire pour réduire les appels à Supabase
class SimpleCache:
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
    
    def get(self, key, max_age_seconds=300):
        """Récupère une valeur du cache si elle n'est pas expirée"""
        if key not in self.cache:
            return None
        
        # Vérifier si le cache est expiré
        if key in self.timestamps:
            age = (datetime.utcnow() - self.timestamps[key]).total_seconds()
            if age > max_age_seconds:
                # Cache expiré, le supprimer
                del self.cache[key]
                del self.timestamps[key]
                return None
        
        return self.cache[key]
    
    def set(self, key, value):
        """Stocke une valeur dans le cache"""
        self.cache[key] = value
        self.timestamps[key] = datetime.utcnow()
    
    def clear(self, key=None):
        """Vide le cache (tout ou une clé spécifique)"""
        if key:
            if key in self.cache:
                del self.cache[key]
            if key in self.timestamps:
                del self.timestamps[key]
        else:
            self.cache.clear()
            self.timestamps.clear()

# Initialiser le cache global
app_cache = SimpleCache()

# Ajouter un filtre pour encoder les URLs
@app.template_filter('urlencode')
def urlencode_filter(s):
    """Encode une chaîne pour l'utiliser dans une URL"""
    if s is None:
        return s
    return quote(str(s))

# Modèle de base de données pour les abonnés newsletter
class AbonneNewsletter(db.Model):
    __tablename__ = 'abonne_newsletter'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def __repr__(self):
        return f'<AbonneNewsletter {self.email}>'

# Modèle de base de données pour les avis clients
class AvisClient(db.Model):
    __tablename__ = 'avis_client'
    
    id = db.Column(db.Integer, primary_key=True)
    nom_complet = db.Column(db.String(100), nullable=False)
    avis = db.Column(db.Text, nullable=False)
    note = db.Column(db.Integer, nullable=False, default=5)  # Note sur 5
    date_creation = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    approuve = db.Column(db.Boolean, default=True, nullable=False)  # Pour modération si nécessaire
    
    def __repr__(self):
        return f'<AvisClient {self.nom_complet}>'

# ========== Fonctions Supabase pour la newsletter ==========

def add_newsletter_subscriber_supabase(email):
    """Ajoute un abonné à la newsletter dans Supabase"""
    if not supabase:
        return False, "Supabase non configuré"
    
    try:
        # Vérifier si l'email existe déjà
        existing = supabase.table('abonne_newsletter').select('email').eq('email', email).execute()
        
        if existing.data and len(existing.data) > 0:
            return False, "Cet email est déjà inscrit à la newsletter"
        
        # Ajouter le nouvel abonné
        data = {
            'email': email,
            'date_inscription': datetime.utcnow().isoformat()
        }
        response = supabase.table('abonne_newsletter').insert(data).execute()
        return True, "Inscription réussie"
    except Exception as e:
        print(f"Erreur lors de l'ajout d'abonné newsletter dans Supabase: {e}")
        return False, str(e)

def get_all_newsletter_subscribers_supabase():
    """Récupère tous les abonnés à la newsletter depuis Supabase"""
    if not supabase:
        return []
    
    try:
        response = supabase.table('abonne_newsletter').select('*').order('date_inscription', desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Erreur lors de la récupération des abonnés newsletter depuis Supabase: {e}")
        return []

def delete_newsletter_subscriber_supabase(email):
    """Supprime un abonné de la newsletter dans Supabase"""
    if not supabase:
        return False, "Supabase non configuré"
    
    try:
        response = supabase.table('abonne_newsletter').delete().eq('email', email).execute()
        return True, "Abonné supprimé avec succès"
    except Exception as e:
        print(f"Erreur lors de la suppression d'abonné newsletter dans Supabase: {e}")
        return False, str(e)

# ========== Fonctions Supabase pour les avis clients ==========

def get_avis_from_supabase(limit=12):
    """Récupère les avis clients depuis Supabase avec cache"""
    if not supabase:
        return []
    
    # Vérifier le cache d'abord (5 minutes)
    cache_key = f'avis_clients_{limit}'
    cached_data = app_cache.get(cache_key, max_age_seconds=300)
    if cached_data is not None:
        return cached_data
    
    try:
        response = supabase.table('avis_clients').select('*').eq('approuve', True).order('date_creation', desc=True).limit(limit).execute()
        # Mettre en cache le résultat
        app_cache.set(cache_key, response.data)
        return response.data
    except Exception as e:
        print(f"Erreur lors de la récupération des avis depuis Supabase: {e}")
        return []

def create_avis_in_supabase(nom_complet, avis, note):
    """Crée un nouvel avis client dans Supabase"""
    if not supabase:
        return False, "Supabase non configuré"
    
    try:
        data = {
            'nom_complet': nom_complet,
            'avis': avis,
            'note': note,
            'date_creation': datetime.utcnow().isoformat(),
            'approuve': True
        }
        response = supabase.table('avis_clients').insert(data).execute()
        # Invalider le cache des avis
        app_cache.clear('avis_clients_12')
        return True, "Avis créé avec succès"
    except Exception as e:
        print(f"Erreur lors de la création de l'avis dans Supabase: {e}")
        return False, str(e)

def get_avis_clients(limit=12):
    """Récupère les avis clients - utilise Supabase si disponible, sinon SQLite"""
    if supabase:
        # Utiliser Supabase
        avis_data = get_avis_from_supabase(limit)
        # Convertir les données Supabase en objets similaires à SQLAlchemy pour compatibilité template
        class AvisObject:
            def __init__(self, data):
                self.id = data.get('id')
                self.nom_complet = data.get('nom_complet')
                self.avis = data.get('avis')
                self.note = data.get('note')
                # Convertir la date string en datetime
                date_str = data.get('date_creation')
                if isinstance(date_str, str):
                    self.date_creation = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    self.date_creation = datetime.utcnow()
                self.approuve = data.get('approuve', True)
        
        return [AvisObject(avis) for avis in avis_data]
    else:
        # Fallback sur SQLite
        return AvisClient.query.filter_by(approuve=True).order_by(AvisClient.date_creation.desc()).limit(limit).all()

# Fonction pour lister les images dans un dossier
def get_images_from_folder(folder_name):
    """Récupère la liste des images dans un dossier static"""
    folder_path = os.path.join(app.static_folder, folder_name)
    if not os.path.exists(folder_path):
        return []
    
    # Extensions d'images supportées
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.svg', '*.webp']
    images = []
    
    for ext in extensions:
        images.extend(glob.glob(os.path.join(folder_path, ext)))
    
    # Retourner seulement les noms de fichiers
    return [os.path.basename(img) for img in images]

# Fonction pour créer des images de placeholder si elles n'existent pas
def create_placeholder_images():
    """Crée des images SVG de placeholder pour les partenaires et certifications"""
    
    # Liste des partenaires (basée sur les templates)
    partenaires = [
        'aibd', 'air liquide', 'anglogold', 'ansd', 'apm terminals', 'boa', 'bollore', 
        'cat', 'cbi', 'cde', 'ciments du sahel', 'coris bank', 'diamond bank', 
        'ecobank', 'enda', 'giz', 'iam', 'ics', 'ird', 'kirene', 'lonase', 
        'orange', 'pcci', 'petrosen', 'sde', 'sen eau', 'sgbs', 'sonatel', 
        'total', 'ucad', 'uemoa', 'unesco', 'usaid'
    ]
    
    # Liste des certifications (basée sur les templates)
    certifications = [
        'apics', 'british', 'cambridge', 'cgeit', 'cisaf', 'cobit', 'comptia', 
        'ec council', 'google', 'iiba', 'isaca', 'iso', 'itil', 'microsoft', 
        'pmi', 'prince2', 'safe', 'scrum', 'toefl', 'toeic'
    ]
    
    # Créer les dossiers s'ils n'existent pas
    os.makedirs(os.path.join(app.static_folder, 'partenaires'), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, 'certifications'), exist_ok=True)
    
    # Créer les images de partenaires
    for partner in partenaires:
        filepath = os.path.join(app.static_folder, 'partenaires', f'{partner}.svg')
        if not os.path.exists(filepath):
            svg_content = f'''<svg width="120" height="60" xmlns="http://www.w3.org/2000/svg">
  <rect width="120" height="60" fill="#f8f9fa" stroke="#e9ecef" stroke-width="1" rx="8"/>
  <text x="60" y="35" font-family="Arial, sans-serif" font-size="12" font-weight="bold" text-anchor="middle" fill="#495057">{partner.upper()}</text>
</svg>'''
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg_content)
    
    # Créer les images de certifications
    for cert in certifications:
        filepath = os.path.join(app.static_folder, 'certifications', f'{cert}.svg')
        if not os.path.exists(filepath):
            svg_content = f'''<svg width="100" height="80" xmlns="http://www.w3.org/2000/svg">
  <rect width="100" height="80" fill="#4169e1" stroke="#2740d1" stroke-width="2" rx="8"/>
  <text x="50" y="45" font-family="Arial, sans-serif" font-size="10" font-weight="bold" text-anchor="middle" fill="white">{cert.upper()}</text>
</svg>'''
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg_content)


@app.route('/')
def home():
    """Affiche la page d'accueil."""
    # Fonction de création de SVG désactivée - utilisation des vraies images PNG uniquement
    
    # Récupérer les avis clients approuvés pour affichage (Supabase ou SQLite)
    avis_clients = get_avis_clients(limit=12)
    
    # Récupérer les listes d'images
    partners_images = get_images_from_folder('images')
    certifications_images = get_images_from_folder('logos')
    
    # Formations en cours (exemples)
    def get_upcoming_trainings():
        items = [
            {"date": datetime(2025, 1, 19), "title": "PMP® : Project Management Professional", "location": "TOGO", "status": "Confirmée"},
            {"date": datetime(2025, 2, 3), "title": "ITIL® 4 Foundation – Préparation", "location": "TOGO", "status": "Ouverte"},
            {"date": datetime(2025, 2, 10), "title": "Scrum Master (PSM)", "location": "TOGO", "status": "Ouverte"},
            {"date": datetime(2025, 3, 5), "title": "ISO 27001 – Introduction", "location": "TOGO", "status": "Ouverte"},
            # Ajouts demandés
            {"date": datetime(2025, 3, 12), "title": "Anglais professionnel & académique", "location": "TOGO", "status": "Ouverte"},
            {"date": datetime(2025, 3, 19), "title": "Business English & spécialisé", "location": "TOGO", "status": "Ouverte"},
            {"date": datetime(2025, 3, 26), "title": "Préparation TOEFL, TOEIC, TFI, IELTS, Cambridge", "location": "TOGO", "status": "Ouverte"},
            {"date": datetime(2025, 4, 2), "title": "Relation client & éducation financière", "location": "TOGO", "status": "Ouverte"},
            {"date": datetime(2025, 4, 9), "title": "Négociation & techniques de vente", "location": "TOGO", "status": "Ouverte"},
            {"date": datetime(2025, 4, 16), "title": "Leadership commercial", "location": "TOGO", "status": "Ouverte"},
            {"date": datetime(2025, 4, 23), "title": "Séminaires & Team Building", "location": "TOGO", "status": "Ouverte"},
        ]
        for it in items:
            try:
                it["month"] = it["date"].strftime('%b').upper()
                it["day"] = it["date"].strftime('%d')
            except Exception:
                it["month"], it["day"] = "", ""
        return items

    upcoming_trainings = get_upcoming_trainings()

    return render_template('index.html', 
                         avis_clients=avis_clients,
                         partners_images=partners_images,
                         certifications_images=certifications_images,
                         upcoming_trainings=upcoming_trainings)

@app.route('/mission')
def mission():
    return render_template('mission.html')

@app.route('/formations')
def formations():
    # Fonction de création de SVG désactivée - utilisation des vraies images PNG uniquement
    
    # Récupérer les listes d'images
    partners_images = get_images_from_folder('images')
    certifications_images = get_images_from_folder('logos')
    
    return render_template('formations.html',
                         partners_images=partners_images,
                         certifications_images=certifications_images)

@app.route('/catalogue-2025')
def catalogue_2025():
    """Alias SEO vers le catalogue 2025."""
    # Fonction de création de SVG désactivée - utilisation des vraies images PNG uniquement
    
    # Récupérer les listes d'images
    partners_images = get_images_from_folder('images')
    certifications_images = get_images_from_folder('logos')
    
    return render_template('formations.html',
                         partners_images=partners_images,
                         certifications_images=certifications_images)


@app.route('/secteurs')
def secteurs():
    return render_template('secteurs.html')


@app.route('/solutions')
def solutions():
    # Fonction de création de SVG désactivée - utilisation des vraies images PNG uniquement
    
    # Récupérer les listes d'images
    partners_images = get_images_from_folder('images')
    certifications_images = get_images_from_folder('logos')
    
    return render_template('solutions.html',
                         partners_images=partners_images,
                         certifications_images=certifications_images)


@app.route('/modalites')
def modalites():
    return render_template('modalites.html')



@app.route('/ressources')
def ressources():
    return render_template('ressources.html')


@app.route('/a-propos')
def apropos():
    return render_template('apropos.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/evenements')
def evenements():
    return render_template('evenements.html')


@app.route('/faq')
def faq():
    return render_template('faq.html')


def build_catalog():
    """Retourne un catalogue unifié: catégories et cours identifiés par des slugs."""
    def course(slug, badge, title, duration, modalities, tags, excerpt, image, cats=""):
        return {
            'slug': slug, 'badge': badge, 'title': title, 'duration': duration,
            'modalities': modalities, 'tags': tags, 'excerpt': excerpt,
            'image': image, 'cats': cats
        }

    tech_courses = [
        course('parcours-acculturer-ia', 'IA', 'Parcours Acculturer', '2.5 heures', ['Elearning','Présentiel','Visioformation'], ['FNE','OPCO','Plan'], "Comprendre les concepts de l’IA générative et ses usages métiers.", 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?auto=format&fit=crop&w=1200&q=80', 'IA Acculturer'),
        course('ia-productivite', 'IA', 'Acculturer et Utiliser – Productivité', '7 heures', ['Elearning','Visioformation'], ['Actions CA','FNE','Plan'], "Utiliser l’IA générative pour booster la productivité.", 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=1200&q=80', 'IA Booster'),
        course('ia-creativite', 'IA', 'Acculturer et Utiliser – Créativité', '7 heures', ['Elearning','Visioformation'], ['FNE','OPCO','Plan'], "Stimuler l’innovation et la création avec l’IA générative.", 'https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1200&q=80', 'IA Booster'),
        course('cyber-fondamentaux', 'Sécurité', 'Cybersécurité – Fondamentaux', '1 jour', ['Présentiel','Visioformation'], ['FNE','OPCO'], "Bonnes pratiques et réduction des risques.", 'https://images.unsplash.com/photo-1556157382-97eda2d62296?auto=format&fit=crop&w=1200&q=80', 'Cybersécurité'),
        course('cloud-decouverte', 'Cloud', 'Découvrir le Cloud & la Virtualisation', '1 jour', ['Présentiel'], ['Plan'], "Comprendre AWS/Azure/GCP et leurs cas d’usage.", 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=1200&q=80', 'Cloud'),
        course('itil4-foundation-prep', 'Gouvernance', 'ITIL® 4 Foundation – Préparation', '2 jours', ['Présentiel','Visioformation'], ['Certification'], "Se préparer à la certification ITIL® 4 Foundation.", 'https://images.unsplash.com/photo-1517245386807-bb43f82c33c4?auto=format&fit=crop&w=1200&q=80', 'Gouvernance IT'),
        course('cobit2019-intro', 'Gouvernance', 'COBIT® 2019 – Introduction', '2 jours', ['Présentiel','Visioformation'], ['Gouvernance'], "Principes et composantes COBIT® 2019.", 'https://images.unsplash.com/photo-1558959357-685f9c7ace7b?auto=format&fit=crop&w=1200&q=80', 'Gouvernance IT'),
        course('toGAF9-fondation', 'Architecture', 'TOGAF® 9 – Fondation', '3 jours', ['Présentiel'], ['Architecture'], "Cadre d’architecture d’entreprise.", 'https://images.unsplash.com/photo-1518779578993-ec3579fee39f?auto=format&fit=crop&w=1200&q=80', 'Gouvernance IT'),
        course('soc-siem-init', 'Sécurité', 'SOC & SIEM – Initiation', '2 jours', ['Présentiel'], ['Sécurité'], "Surveillance, détection et réponse.", 'https://images.unsplash.com/photo-1504639725590-34d0984388bd?auto=format&fit=crop&w=1200&q=80', 'Cybersécurité'),
    ]

    mgmt_courses = [
        course('pmp-preparation', 'PMP', 'PMP® (PMI) – Préparation', '5 jours', ['Présentiel','Visioformation'], ['Certification'], "Se préparer à l’examen PMP®.", 'https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1200&q=80', 'PMP'),
        course('prince2-practitioner', 'Prince2', 'Prince2® Practitioner', '3 jours', ['Présentiel','Visioformation'], ['Certification'], "Approfondir la méthode Prince2®.", 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?auto=format&fit=crop&w=1200&q=80', 'Prince2'),
        course('scrum-master-psm', 'Agile', 'Scrum Master (PSM)', '2 jours', ['Présentiel','Visioformation'], ['Agile'], "Maîtriser Scrum en tant que Scrum Master.", 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=1200&q=80', 'Scrum'),
        course('safe-po-pm', 'SAFe', 'SAFe® Product Owner / Product Manager', '2 jours', ['Présentiel','Visioformation'], ['SAFe'], "Rôles PO/PM dans SAFe®.", 'https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=1200&q=80', 'SAFe'),
        course('kanban-essentiels', 'Agile', 'Kanban – Essentiels', '1 jour', ['Présentiel'], ['Agile'], "Flux tiré et amélioration continue.", 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80', 'Agile'),
        course('lean-six-sigma-green-belt', 'LSS', 'Lean Six Sigma – Green Belt', '5 jours', ['Présentiel','Visioformation'], ['LSS'], "DMAIC et outillage statistique.", 'https://images.unsplash.com/photo-1520975693416-35a0d2c7f59b?auto=format&fit=crop&w=1200&q=80', 'Lean Six Sigma'),
    ]

    iso_courses = [
        course('iso-9001-bases', 'ISO', 'ISO 9001 – Bases', '2 jours', ['Présentiel','Visioformation'], ['Qualité'], "Mettre en place un SMQ.", 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80', 'ISO 9001'),
        course('iso-27001-intro', 'ISO', 'ISO 27001 – Introduction', '2 jours', ['Présentiel'], ['Sécurité'], "SMSI et bonnes pratiques.", 'https://images.unsplash.com/photo-1510511459019-5dda7724fd87?auto=format&fit=crop&w=1200&q=80', 'ISO 27001'),
        course('iso-45001-sst', 'ISO', 'ISO 45001 – SST', '2 jours', ['Présentiel'], ['SST'], "Santé & sécurité au travail.", 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80', 'ISO 45001'),
        course('nebosh-igc', 'NEBOSH', 'NEBOSH IGC – Préparation', '5 jours', ['Présentiel','Visioformation'], ['Certification'], "Préparer la certification IGC.", 'https://images.unsplash.com/photo-1536250853074-24cd68fbe7b7?auto=format&fit=crop&w=1200&q=80', 'NEBOSH'),
        course('iso-50001-energie', 'ISO', 'ISO 50001 – Management de l’énergie', '2 jours', ['Présentiel'], ['Énergie'], "Système de management de l’énergie.", 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1200&q=80', 'ISO 50001'),
        course('iso-20121-evenementiel', 'ISO', 'ISO 20121 – Événementiel responsable', '2 jours', ['Présentiel'], ['RSE'], "Événementiel durable et responsable.", 'https://images.unsplash.com/photo-1497366216548-37526070297c?auto=format&fit=crop&w=1200&q=80', 'ISO 20121'),
    ]

    metiers_courses = [
        course('banque-risque', 'Banque', 'Gestion des risques bancaires', '2 jours', ['Présentiel'], ['Banque'], "Comprendre Bâle II/III et le risque.", 'https://images.unsplash.com/photo-1526304640581-d334cdbbf45e?auto=format&fit=crop&w=1200&q=80', 'Banque & Assurance'),
        course('compta-audit', 'Audit', 'Contrôle interne & Audit', '2 jours', ['Présentiel'], ['Audit'], "Outillage du contrôle interne.", 'https://images.unsplash.com/photo-1454165205744-3b78555e5572?auto=format&fit=crop&w=1200&q=80', 'Comptabilité & Audit'),
        course('supplychain-apics', 'Logistique', 'Supply Chain & APICS', '2 jours', ['Présentiel'], ['APICS'], "Découvrir CPIM/CSCP.", 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?auto=format&fit=crop&w=1200&q=80', 'Logistique & Achats'),
        course('industrie-hse', 'Industrie', 'Management HSE', '2 jours', ['Présentiel'], ['HSE'], "Mettre en place un système HSE.", 'https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1200&q=80', 'Industrie'),
        course('petrole-gaz-normes', 'Énergie', 'Pétrole, Gaz & Mines – Normes', '2 jours', ['Présentiel'], ['Secteur'], "Normes sectorielles et HSE.", 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80', 'Pétrole, Gaz & Mines'),
    ]

    commercial_courses = [
        course('negociation-avancee', 'Vente', 'Négociation avancée', '2 jours', ['Présentiel','Visioformation'], ['Vente'], "Techniques de négociation et closing.", 'https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1200&q=80', 'Négociation'),
        course('relation-client', 'Vente', 'Développer la relation client', '1 jour', ['Présentiel'], ['Client'], "Fidélisation & expérience client.", 'https://images.unsplash.com/photo-1520975693416-35a0d2c7f59b?auto=format&fit=crop&w=1200&q=80', 'Relation client'),
        course('leadership-commercial', 'Management', 'Leadership commercial', '2 jours', ['Présentiel'], ['Vente'], "Piloter une équipe commerciale.", 'https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80', 'Leadership commercial'),
        course('seminaires-team-building', 'RH', 'Séminaires & Team Building', '1 jour', ['Présentiel'], ['Equipe'], "Cohésion et motivation.", 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1200&q=80', 'Team Building'),
    ]

    langues_courses = [
        course('anglais-pro', 'Anglais', 'Anglais professionnel', 'À partir de 7h', ['Elearning','Présentiel','Visioformation'], ['Certifications'], "Améliorer sa communication pro en anglais.", 'https://images.unsplash.com/photo-1517486808906-6ca8b3f04846?auto=format&fit=crop&w=1200&q=80', 'Anglais pro'),
        course('business-english', 'Anglais', 'Business English & spécialisé', 'À partir de 7h', ['Elearning','Visioformation'], ['Certifications'], "Anglais pour banque, commerce, technique.", 'https://images.unsplash.com/photo-1519337265831-281ec6cc8514?auto=format&fit=crop&w=1200&q=80', 'Business English'),
        course('prep-certifications-english', 'Anglais', 'Préparation TOEFL/TOEIC/IELTS/Cambridge', 'À partir de 14h', ['Elearning','Présentiel'], ['Certifications'], "Préparer les certifications internationales.", 'https://images.unsplash.com/photo-1503676260728-1c00da094a0b?auto=format&fit=crop&w=1200&q=80', 'Préparation'),
    ]

    categories = {
        'tech': {
            'title': "Technologies Numériques & Cybersécurité",
            'kicker': 'Catalogue',
            'lead': "Gouvernance, sécurité, cloud et IA générative pour accélérer vos transformations.",
            'image': 'https://images.unsplash.com/photo-1542751371-adc38448a05e?auto=format&fit=crop&w=1400&q=80',
            'filters': ['IA', 'Acculturer', 'Booster', 'Cybersécurité', 'Cloud', 'Gouvernance IT'],
            'courses': tech_courses
        },
        'management': {
            'title': "Gestion de Projet, Management & Leadership",
            'kicker': 'Catalogue',
            'lead': "Des certifications et méthodes pour piloter, transformer et aligner les équipes.",
            'image': 'https://images.unsplash.com/photo-1552664730-d307ca884978?auto=format&fit=crop&w=1400&q=80',
            'filters': ['PMP', 'Prince2', 'Agile', 'Scrum', 'SAFe', 'Lean Six Sigma'],
            'courses': mgmt_courses
        },
        'iso': {
            'title': "Normes ISO & QSSE",
            'kicker': 'Catalogue',
            'lead': "Mettre en place et auditer des systèmes certifiables au meilleur niveau.",
            'image': 'https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?auto=format&fit=crop&w=1400&q=80',
            'filters': ['ISO 9001', 'ISO 14001', 'ISO 45001', 'ISO 50001', 'ISO 20121', 'ISO 27001'],
            'courses': iso_courses
        },
        'metiers': {
            'title': "Filières Métiers",
            'kicker': 'Catalogue',
            'lead': "Des contenus adaptés à vos enjeux par secteur.",
            'image': 'https://images.unsplash.com/photo-1508385082359-f38ae991e8f2?auto=format&fit=crop&w=1400&q=80',
            'filters': ['Banque & Assurance', 'Comptabilité & Audit', 'Logistique & Achats', 'Industrie', 'Pétrole, Gaz & Mines'],
            'courses': metiers_courses
        },
        'commercial': {
            'title': "Performance Commerciale",
            'kicker': 'Catalogue',
            'lead': "Des parcours orientés résultats pour élever l’efficacité commerciale.",
            'image': 'https://images.unsplash.com/photo-1542744173-05336fcc7ad4?auto=format&fit=crop&w=1400&q=80',
            'filters': ['Relation client', 'Négociation', 'Leadership commercial', 'Team Building'],
            'courses': commercial_courses
        },
        'langues': {
            'title': "Langues",
            'kicker': 'Catalogue',
            'lead': "Des parcours d’anglais professionnel et de préparation aux certifications.",
            'image': 'https://images.unsplash.com/photo-1522075469751-3a6694fb2f61?auto=format&fit=crop&w=1400&q=80',
            'filters': ['Anglais pro', 'Business English', 'Préparation certifications'],
            'courses': langues_courses
        }
    }
    return categories


def find_course_by_slug(slug: str):
    cats = build_catalog()
    for cat in cats.values():
        for c in cat['courses']:
            if c['slug'] == slug:
                return c, cat
    return None, None


@app.route('/formations/<category_slug>')
def formation_category(category_slug: str):
    """Page catégorie de formations avec liste de cours et filtres."""
    categories = build_catalog()
    data = categories.get(category_slug)
    if not data:
        return render_template('formations.html')
    return render_template('formation_category.html', category_slug=category_slug, data=data)


@app.route('/formation/<course_slug>')
def formation_detail(course_slug: str):
    """Fiche formation détaillée: affiche uniquement la formation cliquée."""
    course, category = find_course_by_slug(course_slug)
    if not course:
        return render_template('formations.html')
    return render_template('formation_detail.html', course=course, category=category)


@app.route('/newsletter', methods=['POST'])
def newsletter():
    """Route pour l'abonnement à la newsletter"""
    # Récupérer l'email depuis le formulaire ou JSON
    email = request.form.get('email') or (request.json.get('email') if request.is_json else None)
    
    if not email:
        return jsonify({"ok": False, "error": "Adresse email requise"}), 400
    
    # Validation basique de l'email
    if '@' not in email or '.' not in email:
        return jsonify({"ok": False, "error": "Adresse email invalide"}), 400
    
    try:
        email_clean = email.lower().strip()
        
        if supabase:
            # Utiliser Supabase
            success, message = add_newsletter_subscriber_supabase(email_clean)
            
            if success:
                return jsonify({
                    "ok": True, 
                    "message": "Inscription réussie ! Merci de vous être abonné à notre newsletter."
                })
            else:
                # Vérifier si c'est une erreur de doublon
                if "déjà inscrit" in message:
                    return jsonify({
                        "ok": False, 
                        "error": message,
                        "already_subscribed": True
                    }), 409
                else:
                    return jsonify({
                        "ok": False, 
                        "error": message
                    }), 500
        else:
            # Fallback sur SQLite
            # Vérifier si l'email existe déjà
            abonne_existant = AbonneNewsletter.query.filter_by(email=email_clean).first()
            
            if abonne_existant:
                return jsonify({
                    "ok": False, 
                    "error": "Cet email est déjà abonné à notre newsletter",
                    "already_subscribed": True
                }), 409
            
            # Créer un nouvel abonné
            nouvel_abonne = AbonneNewsletter(email=email_clean)
            db.session.add(nouvel_abonne)
            db.session.commit()
            
            return jsonify({
                "ok": True, 
                "message": "Inscription réussie ! Merci de vous être abonné à notre newsletter."
            })
        
    except Exception as e:
        if not supabase:
            db.session.rollback()
        print(f"Erreur lors de l'inscription newsletter: {e}")
        return jsonify({
            "ok": False, 
            "error": "Une erreur s'est produite. Veuillez réessayer plus tard."
        }), 500


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    success = None
    errors = {}
    form_data = {"name": "", "email": "", "subject": "", "message": ""}
    avis_success = None
    avis_errors = {}
    avis_data = {"nom_complet": "", "avis": "", "note": "5"}
    
    if request.method == 'POST':
        # Vérifier quel formulaire a été soumis
        if 'contact_form' in request.form:
            # Traitement du formulaire de contact
            form_data['name'] = request.form.get('name', '').strip()
            form_data['email'] = request.form.get('email', '').strip()
            form_data['subject'] = request.form.get('subject', '').strip()
            form_data['message'] = request.form.get('message', '').strip()

            # Validation
            if not form_data['name']:
                errors['name'] = "Le nom est requis."
            if not form_data['email']:
                errors['email'] = "L'email est requis."
            elif '@' not in form_data['email']:
                errors['email'] = "Veuillez entrer une adresse email valide."
            if not form_data['message']:
                errors['message'] = "Le message est requis."

            # Si pas d'erreurs, envoyer l'email
            if len(errors) == 0:
                try:
                    # Créer le message email
                    subject = form_data['subject'] if form_data['subject'] else "Nouveau message depuis le site Conseilux"
                    
                    msg = Message(
                        subject=f"[Contact Site] {subject}",
                        recipients=[os.environ.get('CONTACT_EMAIL', 'contact@conseiluxtraining.com')],
                        reply_to=form_data['email']
                    )
                    
                    # Corps du message
                    msg.body = f"""Nouveau message reçu depuis le formulaire de contact du site Conseilux Training & Developpement:

Nom: {form_data['name']}
Email: {form_data['email']}
Sujet: {form_data['subject'] if form_data['subject'] else 'Non spécifié'}

Message:
{form_data['message']}

---
Ce message a été envoyé automatiquement depuis le site web."""
                    
                    # Envoyer l'email
                    mail.send(msg)
                    success = True
                    
                    # Réinitialiser le formulaire après envoi réussi
                    form_data = {"name": "", "email": "", "subject": "", "message": ""}
                    
                except Exception as e:
                    success = False
                    errors['general'] = "Une erreur s'est produite lors de l'envoi du message. Veuillez réessayer plus tard."
                    print(f"Erreur envoi email: {e}")  # Pour le debug
            else:
                success = False
        
        elif 'avis_form' in request.form:
            # Traitement du formulaire d'avis
            avis_data['nom_complet'] = request.form.get('nom_complet', '').strip()
            avis_data['avis'] = request.form.get('avis', '').strip()
            avis_data['note'] = request.form.get('note', '5')
            
            # Validation
            if not avis_data['nom_complet']:
                avis_errors['nom_complet'] = "Le nom complet est requis."
            if not avis_data['avis']:
                avis_errors['avis'] = "L'avis est requis."
            if not avis_data['note'] or not avis_data['note'].isdigit() or int(avis_data['note']) < 1 or int(avis_data['note']) > 5:
                avis_errors['note'] = "Veuillez sélectionner une note entre 1 et 5."
            
            # Si pas d'erreurs, enregistrer l'avis
            if len(avis_errors) == 0:
                try:
                    if supabase:
                        # Utiliser Supabase
                        success_flag, message = create_avis_in_supabase(
                            avis_data['nom_complet'],
                            avis_data['avis'],
                            int(avis_data['note'])
                        )
                        avis_success = success_flag
                        if not success_flag:
                            avis_errors['general'] = f"Erreur Supabase: {message}"
                    else:
                        # Fallback sur SQLite
                        nouvel_avis = AvisClient(
                            nom_complet=avis_data['nom_complet'],
                            avis=avis_data['avis'],
                            note=int(avis_data['note'])
                        )
                        db.session.add(nouvel_avis)
                        db.session.commit()
                        avis_success = True
                    
                    # Réinitialiser le formulaire après envoi réussi
                    if avis_success:
                        avis_data = {"nom_complet": "", "avis": "", "note": "5"}
                    
                except Exception as e:
                    if not supabase:
                        db.session.rollback()
                    avis_success = False
                    avis_errors['general'] = "Une erreur s'est produite lors de l'enregistrement de votre avis. Veuillez réessayer plus tard."
                    print(f"Erreur enregistrement avis: {e}")
            else:
                avis_success = False

    return render_template('contact.html', 
                         success=success, errors=errors, form_data=form_data,
                         avis_success=avis_success, avis_errors=avis_errors, avis_data=avis_data)


@app.context_processor
def inject_certifications_images():
    """
    Injecte les images de certifications et partenaires dans tous les templates
    """
    allowed_exts = {'.png', '.jpg', '.jpeg', '.svg', '.webp'}

    # Certifications
    certs_folder = os.path.join(app.static_folder, 'logos')
    certifications_images = []
    try:
        for name in sorted(os.listdir(certs_folder)):
            if os.path.splitext(name)[1].lower() in allowed_exts:
                # Exclure les fichiers de copie et vérifier que le fichier existe
                if '- Copie' not in name and os.path.isfile(os.path.join(certs_folder, name)):
                    certifications_images.append(name)
    except Exception as e:
        print(f"Erreur lors du chargement des certifications: {e}")
        certifications_images = []

    # Partenaires
    partners_folder = os.path.join(app.static_folder, 'images')
    partners_images = []
    try:
        for name in sorted(os.listdir(partners_folder)):
            if os.path.splitext(name)[1].lower() in allowed_exts:
                # Vérifier que le fichier existe
                if os.path.isfile(os.path.join(partners_folder, name)):
                    partners_images.append(name)
    except Exception as e:
        print(f"Erreur lors du chargement des partenaires: {e}")
        partners_images = []

    # Fonction helper pour les chemins statiques compatible Vercel
    def static_url(filename):
        """Génère l'URL statique correcte pour Vercel et local"""
        if os.environ.get('VERCEL'):
            # Sur Vercel, utiliser le chemin absolu
            return f'/static/{filename}'
        else:
            # En local, utiliser url_for
            return url_for('static', filename=filename)
    
    return {
        'certifications_images': certifications_images,
        'partners_images': partners_images,
        'static_url': static_url,
    }

# Filtre personnalisé pour l'encodage des URLs
@app.template_filter('safe_url_encode')
def safe_url_encode(filename):
    """Encode les noms de fichiers pour les URLs de manière sûre"""
    return quote(filename, safe='')

# Route explicite pour servir les fichiers statiques (pour Vercel)
@app.route('/static/<path:filename>')
def serve_static(filename):
    """Sert les fichiers statiques avec gestion des noms avec espaces"""
    try:
        return send_from_directory(app.static_folder, filename)
    except Exception as e:
        print(f"Erreur lors du service du fichier statique {filename}: {e}")
        return "File not found", 404

# Fonction pour initialiser la base de données
def init_db():
    """Initialise la base de données et crée les tables"""
    with app.app_context():
        db.create_all()
        print("Base de données initialisée avec succès")

# Décorateur pour protéger les routes admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Route de connexion admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Page de connexion pour l'administration"""
    if request.method == 'POST':
        password = request.form.get('password')
        if password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_newsletter'))
        else:
            flash('Mot de passe incorrect', 'error')
    
    return render_template('admin_login.html')

# Route de connexion rapide (AJAX)
@app.route('/admin/quick-login', methods=['POST'])
def admin_quick_login():
    """Connexion rapide via AJAX depuis la page d'accueil"""
    data = request.get_json()
    password = data.get('password') if data else None
    
    if password == ADMIN_PASSWORD:
        session['admin_logged_in'] = True
        return jsonify({"ok": True, "message": "Connexion réussie"})
    else:
        return jsonify({"ok": False, "error": "Mot de passe incorrect"}), 401

# Route pour vérifier le statut de connexion
@app.route('/admin/check-status')
def admin_check_status():
    """Vérifie si l'admin est connecté"""
    return jsonify({"logged_in": session.get('admin_logged_in', False)})

# Route de déconnexion admin
@app.route('/admin/logout')
def admin_logout():
    """Déconnexion de l'administration"""
    session.pop('admin_logged_in', None)
    return redirect(url_for('home'))

# Route pour afficher les abonnés (protégée)
@app.route('/admin/newsletter')
@admin_required
def admin_newsletter():
    """Route d'administration pour voir les abonnés (accès protégé)"""
    if supabase:
        # Utiliser Supabase
        abonnes_data = get_all_newsletter_subscribers_supabase()
        # Convertir en objets pour compatibilité template
        class AbonneObject:
            def __init__(self, data):
                self.id = data.get('id')
                self.email = data.get('email')
                date_str = data.get('date_inscription')
                if isinstance(date_str, str):
                    self.date_inscription = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
                else:
                    self.date_inscription = datetime.utcnow()
        
        abonnes = [AbonneObject(a) for a in abonnes_data]
    else:
        # Fallback sur SQLite
        abonnes = AbonneNewsletter.query.order_by(AbonneNewsletter.date_inscription.desc()).all()
    
    return render_template('admin_newsletter.html', abonnes=abonnes)

@app.route('/mentions-legales')
def mentions_legales():
    """Page des mentions légales"""
    return render_template('mentions_legales.html')

@app.route('/politique-confidentialite')
def politique_confidentialite():
    """Page de la politique de confidentialité"""
    return render_template('politique_confidentialite.html')

@app.route('/conditions-generales')
def conditions_generales():
    """Page des conditions générales d'utilisation"""
    return render_template('conditions_generales.html')

# Initialiser la base de données au démarrage de l'application
try:
    init_db()
except Exception as e:
    print(f"Erreur lors de l'initialisation de la base de données: {e}")

if __name__ == '__main__':
    # Lancer le serveur de développement Flask
    # Accessible sur http://127.0.0.1:5000
    app.run(debug=True)
