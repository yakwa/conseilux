import os
import sys

# Ajouter le répertoire parent au PYTHONPATH
parent_dir = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, parent_dir)

# Changer le répertoire de travail vers le parent
os.chdir(parent_dir)

from main import app

# Point d'entrée pour Vercel
# Vercel cherche automatiquement api/index.py
