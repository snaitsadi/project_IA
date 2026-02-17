import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
import numpy as np
from pathlib import Path



# Charger le modèle
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')  # Multilingue, bon pour français/anglais

# Connexion à Qdrant (local)
client = QdrantClient(host="localhost", port=6333)

# Créer une collection pour les freelances
COLLECTION_NAME = "freelances"
VECTOR_SIZE = 512  # Taille des embeddings du modèle choisi

def recreate_collection():
    client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    )

def index_freelances():
    with open("../data/freelances.json", "r") as f:
        freelances = json.load(f)

    points = []
    for f in freelances:
        # Créer un texte combiné pour l'embedding : titre + description + compétences
        text = f"{f['title']} {f['description']} Compétences: {', '.join(f['skills'])}"
        emb = model.encode(text).tolist()
        points.append(PointStruct(
            id=f['id'],
            vector=emb,
            payload={
                "title": f['title'],
                "description": f['description'],
                "skills": f['skills'],
                "city": f['city'],
                "hourly_rate": f['hourly_rate']
            }
        ))

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    print(f"Indexé {len(points)} freelances")

def index_missions_for_eval():
    # Optionnel : indexer aussi les missions pour les utiliser comme requêtes lors de l'évaluation
    with open("../data/missions.json", "r") as f:
        missions = json.load(f)

    # On peut les stocker dans une autre collection ou simplement les garder en mémoire
    # Ici on les sauvegarde dans un fichier numpy pour usage ultérieur
    texts = []
    for m in missions:
        text = f"{m['title']} {m['description']} Compétences requises: {', '.join(m['skills'])}"
        texts.append(text)
    embeddings = model.encode(texts)
    np.save("../data/missions_embeddings.npy", embeddings)
    with open("../data/missions_meta.json", "w") as f:
        json.dump(missions, f, indent=2)
    print("Embeddings des missions sauvegardés")

if __name__ == "__main__":
    recreate_collection()
    index_freelances()
    index_missions_for_eval()