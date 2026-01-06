from typing import Protocol, List
from domain.entities.item import Item

class GetItems(Protocol):
    def execute(self) -> List[Item]: ...