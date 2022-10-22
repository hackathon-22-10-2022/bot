from abc import	ABC

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
	
	async def insert_answer(self, field_object_id: str, user_id: int, answer: list[str] | list[int]) -> str:
		return await self.insert_one({
			'to_field': field_object_id,
			'from': user_id,
			'text': answer,
		})


class MongoFieldsDB(AbstarctMongoDB):
	def __init__(self):
		self.collection = mongo_config.get_mongo_collection_fields()

class MongoUsersDB(AbstarctMongoDB):
	def __init__(self):
		self.collection = mongo_config.get_mongo_collection_users()

class MongoAnswersDB(AbstarctMongoDB):
	def __init__(self):
		self.collection = mongo_config.get_mongo_collection_answers()
