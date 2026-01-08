from features.items.domain.ports.in_ports.get_all_items_port import GetItemsPort
from features.items.domain.ports.out_ports.item_repository_port import ItemRepositoryPort
from features.items.domain.entities.item import Item
from typing import List

class GetItemsUseCase(GetItemsPort):
    def __init__(self, repo: ItemRepositoryPort):
        self.repo = repo

    def execute(self) -> List[Item]:
        items = self.repo.get_all()
        return items