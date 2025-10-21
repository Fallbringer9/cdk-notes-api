
# CDK Notes API — AWS CDK + DynamoDB + Lambda + API Gateway

## 🇫🇷 Version française

Ce projet a été réalisé dans le cadre de mon apprentissage du développement cloud AWS.  
L’objectif est de construire une **API REST complète** en utilisant **AWS CDK (Python)**, avec de bonnes pratiques d’architecture et de sécurité.

L’API permet de créer, lire et supprimer des notes stockées dans **DynamoDB**, à travers des **fonctions AWS Lambda** exposées via **API Gateway**.

### Stack principale
- AWS Lambda — pour exécuter le code backend sans serveur  
- Amazon API Gateway — pour exposer les routes REST (`/notes`, `/notes/{id}`)  
- Amazon DynamoDB — pour stocker les notes (NoSQL, pay-per-request)  
- AWS CDK (Python) — pour décrire et déployer toute l’infrastructure comme du code  
- IAM Roles — pour appliquer le principe du least privilege à chaque Lambda  

### Architecture du projet
```
cdk-notes-api/
│
├── app.py                      # Point d’entrée CDK
├── cdk_notes_api/
│   ├── cdk_notes_api_stack.py  # Infrastructure (CDK)
│   └── ...
│
├── src/
│   ├── create_note/handler.py  # Lambda POST /notes
│   ├── get_note/handler.py     # Lambda GET /notes/{id}
│   └── delete_note/handler.py  # Lambda DELETE /notes/{id}
│
└── requirements.txt
```

### Fonctionnalités
| Méthode | Endpoint | Description |
|----------|-----------|-------------|
| POST | /notes | Crée une note et la stocke dans DynamoDB |
| GET | /notes/{id} | Récupère une note par son ID |
| DELETE | /notes/{id} | Supprime une note existante |

### Objectifs pédagogiques
Ce projet m’a permis de :
- Comprendre la relation entre CDK, Lambda, API Gateway et DynamoDB  
- Manipuler des permissions IAM minimales pour sécuriser les fonctions  
- Tester des endpoints via cURL sans interface graphique  
- Déployer une stack complète AWS en Infrastructure as Code (IaC)  

L’objectif n’est pas la perfection du code, mais la compréhension de la logique AWS et la mise en pratique de CDK Python étape par étape.

---

## 🇬🇧 English version

This project was built as part of my learning journey in AWS Cloud Development.  
It’s a simple serverless REST API using AWS CDK (Python), focused on clarity, security, and infrastructure as code.

### Main stack
- AWS Lambda — serverless backend functions  
- API Gateway — exposes REST routes (`/notes`, `/notes/{id}`)  
- DynamoDB — serverless NoSQL database  
- AWS CDK (Python) — defines and deploys the entire infrastructure  
- IAM Roles — implements least privilege per Lambda  

### Project structure
```
cdk-notes-api/
│
├── app.py
├── cdk_notes_api/
│   └── cdk_notes_api_stack.py
├── src/
│   ├── create_note/handler.py
│   ├── get_note/handler.py
│   └── delete_note/handler.py
└── requirements.txt
```

### Features
| Method | Endpoint | Description |
|---------|-----------|-------------|
| POST | /notes | Create a note |
| GET | /notes/{id} | Retrieve a note |
| DELETE | /notes/{id} | Delete a note |

### Learning focus
This project helped me understand:
- How CDK connects Lambda, API Gateway and DynamoDB  
- How to apply least privilege IAM permissions  
- How to test REST APIs via cURL  
- How to manage infrastructure through code  

It’s not a production-ready system — it’s a learning milestone in my AWS Developer path.