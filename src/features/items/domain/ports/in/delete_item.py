from typing import Protocol

class DeleteItem(Protocol):
    def execute(self, item_id: str) -> bool: ...