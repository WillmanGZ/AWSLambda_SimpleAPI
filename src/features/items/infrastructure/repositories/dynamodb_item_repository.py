import os
import boto3
from botocore.exceptions import ClientError

from features.items.domain.entities.item import Item
from features.items.domain.ports.out_ports.item_repository_port import ItemRepositoryPort
from features.items.infrastructure.mappers.item_mapper import ItemMapper
from typing import List


class DynamoItemRepository(ItemRepositoryPort):
    def __init__(self):
        table_name = os.environ["ITEMS_TABLE"]
        self.table = boto3.resource("dynamodb").Table(table_name)

    def get_all(self) -> List[Item]:
        response = self.table.scan();
        items = response.get("Items", [])
        return [ItemMapper.from_dynamo(item) for item in items]
    

    def get_by_id(self, item_id: str) -> Item | None:
        try:
            response = self.table.get_item(
                Key={"id": item_id}
            )
        except ClientError as e:
            raise RuntimeError(e.response["Error"]["Message"])

        item = response.get("Item")
        if not item:
            return None

        return ItemMapper.from_dynamo(item)
    
    def create(self, item: Item) -> Item:
        try:
            self.table.put_item(
                Item=ItemMapper.to_dynamo(item)
            )
        except ClientError as e:
            raise RuntimeError(e.response["Error"]["Message"])

        return item

    def update(self, item: Item) -> Item | None:
        try:
            self.table.put_item(
                Item=ItemMapper.to_dynamo(item),
                ConditionExpression="attribute_exists(id)"
            )
            return item
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return None
            raise RuntimeError(e.response["Error"]["Message"])


    def delete(self, item_id: str) -> bool:
        try:
            response = self.table.delete_item(
                Key={"id": item_id},
                ConditionExpression="attribute_exists(id)"
            )
            return True
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                return False
            raise RuntimeError(e.response["Error"]["Message"])
