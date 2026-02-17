import json
import random
from pathlib import path 


# Définir les compétences possibles

SKILLS = [
    "python", "Java", "JavaScript", "React", "Node.js", "Django", "Flask",
    "SQL", "NoSQL", "AWS", "Docker", "Kubernetes", "Machine Learning",
    "Data Science", "NLP", "Computer Vision", "DevOps", "CI/CD", "Terraform",
    "GraphQL", "REST API", "FastAPI", "PyTorch", "TensorFlow", "Scikit-learn",
    "Pandas", "NumPy", "BigQuery", "Elasticsearch", "Qdrant", "Kafka"
 ]

#Données des villes
CITIES = ["Paris", "Lyon", "Bordeaux", "Toulouse", "Lille", "Nantes", "Strasbourg", "Rennes"]


# Générer des profils freelances
def generate_freelances(n=1000):
    freelances = []
    for i in range(n):
        num_skills = random.randint(3, 8)
        skills = random.sample(SKILLS, num_skills)
        title = f"{random.choice(['Développeur', 'Ingénieur', 'Consultant', 'Expert'])} {skills[0]}"
        description = f"Freelance avec {random.randint(2, 10)} ans d'expérience. Spécialisé en {', '.join(skills[:3])}. "
        description += f"A travaillé sur des projets dans {random.choice(['la finance', 'la santé', 'le e-commerce', 'les télécoms'])}."
        freelances.append({
            "id": i,
            "title": title,
            "description": description,
            "skills": skills,
            "city": random.choice(CITIES),
            "hourly_rate": random.randint(300, 800)
        })
    return freelances