import json
import random
from pathlib import Path


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



# Générer des missions
def generate_missions(n=200):
    missions = []
    for i in range(n):
        num_skills = random.randint(2, 5)
        skills = random.sample(SKILLS, num_skills)
        title = f"Recherche {random.choice(['un', 'un(e)'])} {skills[0]} Freelance"
        description = f"Mission de {random.randint(1, 12)} mois. "
        description += f"Nous cherchons un expert en {', '.join(skills)} pour "
        description += random.choice([
            "développer une application web.",
            "mettre en place une infrastructure cloud.",
            "créer un modèle de machine learning.",
            "optimiser les performances de nos bases de données.",
            "moderniser notre stack technique."
        ])
        missions.append({
            "id": i,
            "title": title,
            "description": description,
            "skills": skills,
            "duration_months": random.randint(1, 12),
            "budget": random.randint(10000, 100000)
        })
    return missions

if __name__ == "__main__":
    Path("../data").mkdir(exist_ok=True)
    freelances = generate_freelances(1000)
    missions = generate_missions(200)
    with open("../data/freelances.json", "w") as f:
        json.dump(freelances, f, indent=2)
    with open("../data/missions.json", "w") as f:
        json.dump(missions, f, indent=2)
    print("Données générées dans le dossier data/")