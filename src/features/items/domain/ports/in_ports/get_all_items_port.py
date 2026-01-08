from typing import Protocol, List
from features.items.domain.entities.item import Item

class GetItemsPort(Protocol):
    def execute(self) -> List[Item]: ...