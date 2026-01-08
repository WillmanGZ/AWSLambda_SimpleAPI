from features.items.domain.ports.in_ports.create_item_port import CreateItemPort
from features.items.domain.ports.out_ports.item_repository_port import ItemRepositoryPort
from features.items.domain.entities.item import Item
import uuid

class CreateItemUseCase(CreateItemPort):
    def __init__(self, repo: ItemRepositoryPort):
        self.repo = repo

    def execute(self, name:str) -> Item:
        item = self.repo.create(Item(
            id=str(uuid.uuid4()),
            name=name
        ))
        return item