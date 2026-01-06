from domain.ports.in_ports.delete_item_port import DeleteItemPort
from domain.ports.out_ports.item_repository_port import ItemRepositoryPort
from domain.exceptions.item_not_found_exception import ItemNotFoundError

class DeleteItemUseCase(DeleteItemPort):
    def __init__(self, repo: ItemRepositoryPort):
        self.repo = repo

    def execute(self, item_id:str) -> bool:
        item = self.repo.get_by_id(item_id);

        if not item:
            raise ItemNotFoundError(item_id)
        
        self.repo.delete(item_id)
        return True