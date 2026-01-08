import json
from features.items.application.use_cases.get_item_by_id_use_case import GetItemByIdUseCase
from features.items.infrastructure.repositories.dynamodb_item_repository import DynamoItemRepository
from features.items.infrastructure.mappers.item_mapper import ItemMapper


def handler(event, context):
    item_id = event["pathParameters"]["id"]

    repo = DynamoItemRepository()
    use_case = GetItemByIdUseCase(repo)

    item = use_case.execute(item_id)

    if item is None:
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Item not found"})
        }

    return {
        "statusCode": 200,
        "body": json.dumps(item.model_dump())
    }
