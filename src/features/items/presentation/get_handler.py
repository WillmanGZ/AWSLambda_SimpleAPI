import json
from features.items.application.use_cases.get_all_items_use_case import GetItemsUseCase
from features.items.infrastructure.repositories.dynamodb_item_repository import DynamoItemRepository


def handler(event, context):
    repo = DynamoItemRepository()
    use_case = GetItemsUseCase(repo)

    items = use_case.execute()

    return {
        "statusCode": 200,
        "body": json.dumps([item.model_dump() for item in items])
    }