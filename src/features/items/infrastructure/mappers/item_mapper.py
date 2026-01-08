from features.items.domain.entities.item import Item


class ItemMapper:
    @staticmethod
    def to_dynamo(item: Item) -> dict:
        return {
            "id": item.id,
            "name": item.name,
        }

    @staticmethod
    def from_dynamo(data: dict) -> Item:
        return Item(
            id=data["id"],
            name=data["name"],
        )
