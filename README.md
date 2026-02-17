# Projet de Matching Sémantique Freelances/Missions pour Malt

Ce projet a été réalisé dans le cadre d’une candidature pour un stage **Machine Learning Engineer** chez Malt. Il implémente un système de recommandation basé sur des **embeddings sémantiques** pour rapprocher des freelances et des missions, en utilisant une base de données vectorielle (Qdrant) et un modèle de langue multilingue.

## Objectifs

- Créer un jeu de données synthétique de profils freelances et de missions.
- Générer des embeddings sémantiques à l’aide d’un modèle Transformer (Sentence-BERT).
- Indexer les embeddings dans Qdrant pour une recherche rapide par similarité.
- Exposer une API REST (FastAPI) permettant d’interroger les freelances les plus pertinents pour une description de mission donnée.
- Évaluer les performances du système (précision, rappel) sur les données générées.

## Prérequis

- **Python 3.10+** installé.
- **Qdrant** binaire (téléchargé manuellement, car Docker n’était pas utilisable sur l’environnement cible).
- Les dépendances Python listées dans `requirements.txt`.

## Installation

### 1. Cloner le dépôt (ou créer les fichiers manuellement)

```bash
git clone <url>   # ou placez-vous dans le répertoire du projet
cd project_IA



# Créer un environnement virtuel et installer les dépendances


python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt



## installer Qdrant 

Téléchargez la dernière version Linux depuis le site officiel :

wget https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-unknown-linux-gnu.tar.gz
tar -xzf qdrant-x86_64-unknown-linux-gnu.tar.gz
mv qdrant-x86_64-unknown-linux-gnu/qdrant ./
rm -rf qdrant-x86_64-unknown-linux-gnu*

# Rendez-le exécutable :

chmod +x qdrant

# Lancer Qdrant

./qdrant

# Le serveur écoute sur localhost:6333. Laissez ce terminal ouvert ou lancez-le en arrière-plan :


nohup ./qdrant > qdrant.log 2>&1 &

#Génération des données synthétiques
cd scripts
python generate_data.py
#Création des embeddings et indexation
python create_embeddings.py


#Lancement de l’API
cd /autofs/unityaccount/cremi/snaitsadi/project_IA
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

L’API est accessible sur http://localhost:8000. La documentation interactive est disponible sur http://localhost:8000/docs

Exemple de requête
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"mission_description": "Nous recherchons un développeur Python expérimenté en machine learning", "top_k": 5}'

  #Évaluation des performances
  cd scripts
python evaluate.py