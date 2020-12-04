from typing import List, Dict, TypeVar, Type
from abc import ABCMeta, abstractmethod
from database.database import Database

T = TypeVar('T', bound='Model')


class Model(metaclass=ABCMeta):
    collection: str
    _id: str

    def __init__(self):
        pass

    def save_to_db(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    @classmethod
    def find_one_by(cls: Type[T], attribute: str, value: str) -> T:
        return cls(**Database.find_one(cls.collection, {attribute: value}))

    @classmethod
    def all(cls: Type[T]):
        elements_from_db = Database.find(cls.collection, {})
        return list(elements_from_db)