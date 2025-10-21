import os
import json
import uuid
from datetime import datetime, timezone

import boto3

TABLE_NAME = os.environ["NOTES_TABLE"]
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(TABLE_NAME)


def _resp(status: int, body: dict):
    return {
        "statusCode": status,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body),
    }


def handler(event, context):
    try:
        if "body" not in event:
            return _resp(400, {"error": "Missing body"})

        data = json.loads(event["body"] or "{}")

        title = data.get("title")
        content = data.get("content")
        tags = data.get("tags", [])

        if not isinstance(title, str) or not title.strip():
            return _resp(400, {"error": "title (string) is required"})
        if not isinstance(content, str) or not content.strip():
            return _resp(400, {"error": "content (string) is required"})
        if not isinstance(tags, list):
            return _resp(400, {"error": "tags must be a list of strings"})

        # Génération des métadonnées
        note_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        item = {
            "note_id": note_id,
            "title": title.strip(),
            "content": content,
            "tags": tags,
            "createdAt": now,
            "updatedAt": now,
            "version": 1,
        }

        table.put_item(Item=item)

        return _resp(201, {
            "message": "created",
            "note_id": note_id,
            "createdAt": now,
            "version": 1,
        })

    except json.JSONDecodeError:
        return _resp(400, {"error": "invalid JSON"})
    except Exception as e:
        # Logging minimal: les détails complets sont visibles dans CloudWatch
        return _resp(500, {"error": str(e)})