import os
from urllib.parse import quote_plus

from motor import motor_asyncio

from dotenv import load_dotenv

load_dotenv()


class Config:
    def __init__(self):
        self.TELEGRAM_TOKEN_BOT = os.getenv('TELEGRAM_TOKEN_BOT')
        self.MONGO_DB_URL = os.getenv('MONGO_DB_URL')


class MongoConfig:
    @staticmethod
    def get_mongo_client() -> motor_asyncio.AsyncIOMotorClient:
        return motor_asyncio.AsyncIOMotorClient(Config().MONGO_DB_URL)
    
    def get_mongo_collection(self) -> motor_asyncio.AsyncIOMotorCollection:
        return self.get_mongo_client().hackathon_22_10_2022.spetsdor


config = Config()
mongo_config = MongoConfig()


