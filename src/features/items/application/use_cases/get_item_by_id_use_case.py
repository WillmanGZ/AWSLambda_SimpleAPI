from domain.ports.in_ports.get_item_by_id_port import GetItemByIdPort
from domain.ports.out_ports.item_repository_port import ItemRepositoryPort
from domain.entities.item import Item

class GetItemByIdUseCase(GetItemByIdPort):
    def __init__(self, repo: ItemRepositoryPort):
        self.repo = repo

    def execute(self, item_id: str) -> Item | None:
        item = self.repo.get_by_id
        return item