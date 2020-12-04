from dataclasses import dataclass, field
from typing import Dict
from models.model import Model


@dataclass(eq=False)
class Question(Model):
    collection: str = field(init=False)
    query: Dict
