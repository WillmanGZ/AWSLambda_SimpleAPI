from typing import Protocol, List
from domain.entities.item import Item

class GetItemsPort(Protocol):
    def execute(self) -> List[Item]: ...