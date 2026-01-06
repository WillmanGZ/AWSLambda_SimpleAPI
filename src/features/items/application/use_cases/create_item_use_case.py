from domain.ports.in_ports.create_item_port import CreateItemPort
from domain.ports.out_ports.item_repository_port import ItemRepositoryPort
from domain.entities.item import Item

class CreateItemUseCase(CreateItemPort):
    def __init__(self, repo: ItemRepositoryPort):
        self.repo = repo

    def execute(self, name:str) -> Item:
        item = self.repo.create(name)
        return item