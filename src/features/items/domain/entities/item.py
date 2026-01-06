from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Item:
    id: str
    name: str
