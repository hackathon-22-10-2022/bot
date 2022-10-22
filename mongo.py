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


class MongoFieldsDB(AbstarctMongoDB):
	def __init__(self):
		self.collection = mongo_config.get_mongo_collection_fields()

class MongoUsersDB(AbstarctMongoDB):
	def __init__(self):
		self.collection = mongo_config.get_mongo_collection_users()
