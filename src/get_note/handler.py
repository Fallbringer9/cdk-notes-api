import json
import os
import boto3
from decimal import Decimal

TABLE_NAME = os.environ["NOTES_TABLE"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)

# Custom encoder pour Decimal
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

def _resp(status: int, body: dict):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body, cls=DecimalEncoder),
    }

def handler(event, context):
    note_id = (event.get("pathParameters") or {}).get("id")
    if not note_id:
        return _resp(400, {"error": "path parameter {id} is required"})

    try:
        resp = table.get_item(Key={"note_id": note_id})
        item = resp.get("Item")
        if not item:
            return _resp(404, {"error": "note not found", "note_id": note_id})

        return _resp(200, {"note": item})
    except Exception as e:
        return _resp(500, {"error": str(e), "note_id": note_id})