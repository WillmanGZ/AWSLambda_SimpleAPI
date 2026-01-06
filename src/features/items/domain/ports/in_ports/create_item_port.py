from typing import Protocol
from domain.entities.item import Item

class CreateItemPort(Protocol):
    def execute(self, name: str) -> Item: ...