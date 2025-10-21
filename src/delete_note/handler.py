import os
import json
import boto3
from decimal import Decimal

# --- Initialisation globale (exécutée une seule fois par conteneur Lambda)
TABLE_NAME = os.environ["NOTES_TABLE"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


# --- Convertisseur pour les types Decimal (comme pour GET)
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)


# --- Fonction utilitaire : formatage HTTP propre
def _resp(status: int, body: dict | None = None):
    """Retourne une réponse API Gateway standard"""
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body or {}, cls=DecimalEncoder),
    }


# --- Handler principal Lambda
def handler(event, context):
    """
    Supprime une note de la table DynamoDB en fonction de note_id.
    Appelée par DELETE /notes/{id}
    """
    try:
        # 1️⃣ Extraire l'ID depuis le chemin
        note_id = (event.get("pathParameters") or {}).get("id")
        if not note_id:
            return _resp(400, {"error": "path parameter {id} is required"})

        # 2️⃣ Vérifier que l'élément existe avant suppression
        existing = table.get_item(Key={"note_id": note_id}).get("Item")
        if not existing:
            return _resp(404, {"error": "note not found", "note_id": note_id})

        # 3️⃣ Supprimer l'élément
        table.delete_item(Key={"note_id": note_id})

        # 4️⃣ Réponse succès
        return _resp(200, {"deleted": True, "note_id": note_id})

    except Exception as e:
        # 5️⃣ Gestion d’erreur générale
        return _resp(500, {"error": str(e), "note_id": note_id})