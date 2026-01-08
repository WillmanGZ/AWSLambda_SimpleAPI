from typing import Protocol
from features.items.domain.entities.item import Item

class UpdateItemPort(Protocol):
    def execute(self, item_id:str, name: str) -> Item: ...