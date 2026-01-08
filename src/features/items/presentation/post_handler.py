import json
from features.items.application.use_cases.create_item_use_case import CreateItemUseCase
from features.items.infrastructure.repositories.dynamodb_item_repository import DynamoItemRepository


def handler(event, context):
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
    use_case = CreateItemUseCase(repo)

    item = use_case.execute(name)

    return {
        "statusCode": 201,
        "body": json.dumps(item.model_dump())
    }
