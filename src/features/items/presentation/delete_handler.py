import json
from features.items.application.use_cases.delete_item_use_case import DeleteItemUseCase
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

    repo = DynamoItemRepository()
    use_case = DeleteItemUseCase(repo)

    deleted = use_case.execute(item_id)

    if not deleted:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Item not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Item deleted successfully"})
    }
