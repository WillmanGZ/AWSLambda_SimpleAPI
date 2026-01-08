import json
from features.items.application.use_cases.delete_item_use_case import DeleteItemUseCase
from features.items.infrastructure.repositories.dynamodb_item_repository import DynamoItemRepository



def handler(event, context):
    item_id = event["pathParameters"]["id"]

    repo = DynamoItemRepository()
    use_case = DeleteItemUseCase(repo)

    deleted = use_case.execute(item_id)

    if not deleted:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Item not found"})
        }

    return {
        "statusCode": 204,
        "body": ""
    }
