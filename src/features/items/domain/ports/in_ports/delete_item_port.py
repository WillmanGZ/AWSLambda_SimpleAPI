from typing import Protocol

class DeleteItemPort(Protocol):
    def execute(self, item_id: str) -> bool: ...