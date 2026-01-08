from features.items.domain.ports.in_ports.update_item_port import UpdateItemPort
from features.items.domain.ports.out_ports.item_repository_port import ItemRepositoryPort
from features.items.domain.entities.item import Item

class UpdateItemUseCase(UpdateItemPort):
    def __init__(self, repo: ItemRepositoryPort):
        self.repo = repo

    def execute(self, item_id: str, name: str) -> Item | None:
        item_to_update = Item(
            id=item_id,
            name=name
        )
        return self.repo.update(item_to_update)