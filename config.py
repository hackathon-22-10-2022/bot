import os
import json
from urllib.parse import quote_plus

from motor import motor_asyncio

from dotenv import load_dotenv

load_dotenv()


class Config:
    TELEGRAM_TOKEN_BOT = None
    MONGO_DB_URL = None
    PATH_TO_INPUT_DATA = None
    PATH_TO_USERS_FILE_FOLDER = None
    BASE_DIR = None

    def __init__(self):
        self.TELEGRAM_TOKEN_BOT = os.getenv("TELEGRAM_TOKEN_BOT")
        self.MONGO_DB_URL = os.getenv("MONGO_DB_URL")
        self.PATH_TO_INPUT_DATA = "input_data.json"
        self.PATH_TO_USERS_FILE_FOLDER = "files"
        self.BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    def get_input_data(self):
        with open(self.PATH_TO_INPUT_DATA) as f:
            return json.load(f)


class MongoConfig:
    @staticmethod
    def get_mongo_client() -> motor_asyncio.AsyncIOMotorClient:
        return motor_asyncio.AsyncIOMotorClient(Config().MONGO_DB_URL)

    def get_mongo_collection_fields(self) -> motor_asyncio.AsyncIOMotorCollection:
        return self.get_mongo_client().hackathon_22_10_2022.fields

    def get_mongo_collection_users(self) -> motor_asyncio.AsyncIOMotorCollection:
        return self.get_mongo_client().hackathon_22_10_2022.users

    def get_mongo_collection_answers(self) -> motor_asyncio.AsyncIOMotorCollection:
        return self.get_mongo_client().hackathon_22_10_2022.answers

    def get_mongo_collection_ready_from(self) -> motor_asyncio.AsyncIOMotorCollection:
        return self.get_mongo_client().hackathon_22_10_2022.ready_form


config = Config()
mongo_config = MongoConfig()
