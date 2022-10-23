from abc import ABC

from motor import motor_asyncio

from config import mongo_config


class AbstarctMongoDB(ABC):
    def __init__(self):
        self.collection: motor_asyncio.AsyncIOMotorCollection = None

    async def insert_one(self, document: dict) -> str:
        result = await self.collection.insert_one(document)
        return result.inserted_id

    async def find_one(self, filter: dict) -> dict:
        return await self.collection.find_one(filter)

    async def find_many(self, filter: dict) -> list:
        return await self.collection.find(filter).to_list(None)

    async def update_one(self, filter: dict, update: dict) -> dict:
        return await self.collection.update_one(filter, update)

    async def delete_one(self, filter: dict) -> dict:
        return await self.collection.delete_one(filter)

    async def find_all(self) -> list:
        return await self.collection.find().to_list(None)

    async def get_by_field_id(self, _id: str) -> dict:
        return await self.collection.find_one({"_id": _id})


class MongoFieldsDB(AbstarctMongoDB):
    def __init__(self):
        super().__init__()
        self.collection = mongo_config.get_mongo_collection_fields()

    async def get_by_field_number(self, field_id: int) -> dict:
        return await self.collection.find_one({"field_id": field_id})


class MongoUsersDB(AbstarctMongoDB):
    def __init__(self):
        super().__init__()
        self.collection = mongo_config.get_mongo_collection_users()

    async def get_senders(self) -> set[int]:
        objects = await self.find_many({"senders": {"$exists": True}})
        return set(objects[0]["senders"])

    async def get_foremans(self) -> set[int]:
        objects = await self.find_many({"foremans": {"$exists": True}})
        return set(objects[0]["foremans"])


class MongoAnswersDB(AbstarctMongoDB):
    def __init__(self):
        super().__init__()
        self.collection = mongo_config.get_mongo_collection_answers()

    async def insert_answer(
        self, field_object_id: str, user_id: int, answer: list[str] | list[int]
    ) -> str:
        return await self.insert_one(
            {
                "to_field": field_object_id,
                "from": user_id,
                "answer": answer,
            }
        )

    async def get_current_senders(self) -> set[int]:
        current_senders = set()
        objects = await self.find_many({"from": {"$exists": True}})
        for obj in objects:
            current_senders.add(obj["from"])
        return current_senders

    async def get_user_answers(self, user_id: int) -> list[dict]:
        return await self.find_many({"from": user_id})

    async def get_filter_by_to_field(self, to_field: str) -> list[dict]:
        return await self.find_many({"to_field": to_field})


class MongoReadyFormsDB(AbstarctMongoDB):
    def __init__(self):
        super().__init__()
        self.collection = mongo_config.get_mongo_collection_ready_from()
