from typing import Protocol
from domain.entities.item import Item

class CreateItem(Protocol):
    def execute(self, name: str) -> Item: ...