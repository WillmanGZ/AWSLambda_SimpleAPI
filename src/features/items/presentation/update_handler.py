import json
from features.items.application.use_cases.update_item_use_case import UpdateItemUseCase
from features.items.infrastructure.repositories.dynamodb_item_repository import DynamoItemRepository

def handler(event, context):
    try:
        item_id = event["pathParameters"]["id"]

        if not item_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Item id must be provided"})
            }
    except:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Item id must be provided"})
        }

    try:
        body = json.loads(event["body"])
        name = body.get("name")

        if not body or not name:
            return {
                "statusCode": 400,
                "body": json.dumps({"message": "Name is required"})
            }
    except:
        return {
                "statusCode": 400,
                "body": json.dumps({"message": "Name is required"})
            }

    repo = DynamoItemRepository()
    use_case = UpdateItemUseCase(repo)

    item = use_case.execute(item_id, name)

    if item is None:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Item not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(item.model_dump())
    }