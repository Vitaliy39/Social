import os
from typing import Dict
import pymongo


class Database:
    URI = 'mongodb+srv://Sociologist:123@cluster0.ay5o5.mongodb.net/Sociology?retryWrites=true&w=majority'
    DATABASE = pymongo.MongoClient(URI).get_default_database()

    @staticmethod
    def find(collection: str, query: Dict) -> pymongo.cursor:
        return Database.DATABASE[collection].find(query)

    @staticmethod
    def find_one(collection:str, query: Dict) -> Dict:
        return Database.DATABASE[collection].find_one(query)

    @staticmethod
    def create_collection(collection: str):
        Database.DATABASE[collection]
        return None

    @staticmethod
    def insert( collection: str, query: Dict):
        Database.DATABASE[collection].insert(query)

    @staticmethod
    def update(collection: str, query: Dict, data: Dict) -> None:
        Database.DATABASE[collection].update(query, data, upsert=True)

    @staticmethod
    def delete(collection: str, query: Dict) -> None:
        Database.DATABASE[collection].delete_one(query)