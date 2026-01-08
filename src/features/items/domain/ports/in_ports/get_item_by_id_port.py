from typing import Protocol
from features.items.domain.entities.item import Item

class GetItemByIdPort(Protocol):
    def execute(self, item_id: str) -> Item | None: ...