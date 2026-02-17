from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from typing import List, Optional
import uvicorn

app = FastAPI(title="Malt Matching API")

# Charger le modèle et le client Qdrant (au démarrage)
model = SentenceTransformer('distiluse-base-multilingual-cased-v2')
client = QdrantClient(host="localhost", port=6333)
COLLECTION_NAME = "freelances"

class SearchQuery(BaseModel):
    mission_description: str
    top_k: Optional[int] = 10

class FreelanceResult(BaseModel):
    id: int
    title: str
    description: str
    skills: List[str]
    city: str
    hourly_rate: int
    score: float

@app.post("/search", response_model=List[FreelanceResult])
def search_freelances(query: SearchQuery):
    # Générer l'embedding de la mission
    emb = model.encode(query.mission_description).tolist()

    # Utiliser query_points au lieu de search
    response = client.query_points(
        collection_name=COLLECTION_NAME,
        query=emb,                     # paramètre 'query' pour le vecteur
        limit=query.top_k
    )

    # Les résultats sont dans response.points
    output = []
    for res in response.points:
        output.append(FreelanceResult(
            id=res.id,
            title=res.payload["title"],
            description=res.payload["description"],
            skills=res.payload["skills"],
            city=res.payload["city"],
            hourly_rate=res.payload["hourly_rate"],
            score=res.score
        ))
    return output


@app.get("/health")
def health():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
