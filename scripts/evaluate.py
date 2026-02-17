import json
import numpy as np
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from sklearn.metrics import precision_score, recall_score
from tqdm import tqdm

# Charger le modèle et le client
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "freelances"

# Charger les missions et leurs embeddings pré-calculés
missions_emb = np.load("../data/missions_embeddings.npy")
with open("../data/missions_meta.json", "r") as f:
    missions = json.load(f)

# Pour chaque mission, on considère comme "pertinents" les freelances ayant au moins une compétence commune
# (c'est une heuristique simple; dans un vrai projet on utiliserait des données d'interaction)
def get_relevant_freelance_ids(mission):
    required_skills = set(mission['skills'])
    relevant_ids = []
    # On charge tous les freelances (à optimiser avec une requête)
    # Ici on utilise un scan de tous les points (pas efficace pour un grand volume, mais pour l'exemple)
    # En pratique, on utiliserait un filtre ou on chargerait les payloads.
    # Pour l'exemple, on va chercher tous les freelances via scroll.
    all_freelances = []
    next_offset = None
    while True:
        results = client.scroll(collection_name=COLLECTION_NAME, limit=100, offset=next_offset)
        batch, next_offset = results
        all_freelances.extend(batch)
        if next_offset is None:
            break
    for f in all_freelances:
        freelance_skills = set(f.payload['skills'])
        if freelance_skills & required_skills:  # intersection non vide
            relevant_ids.append(f.id)
    return relevant_ids

# Calcul des métriques pour k=10
k = 10
precisions = []
recalls = []

for i, mission in enumerate(tqdm(missions)):
    emb = missions_emb[i].tolist()
    response = client.query_points(collection_name=COLLECTION_NAME, query=emb, limit=k)
    retrieved_ids = [r.id for r in response.points]
    relevant_ids = get_relevant_freelance_ids(mission)

    if len(relevant_ids) == 0:
        continue  # ignorer les missions sans aucun freelance pertinent (rare dans notre génération)

    # Precision@k
    relevant_retrieved = set(retrieved_ids) & set(relevant_ids)
    prec = len(relevant_retrieved) / k
    precisions.append(prec)

    # Recall@k
    rec = len(relevant_retrieved) / len(relevant_ids)
    recalls.append(rec)

print(f"Precision@{k} moyen : {np.mean(precisions):.3f}")
print(f"Recall@{k} moyen    : {np.mean(recalls):.3f}")