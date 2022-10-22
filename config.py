import imp
import os
from urllib.parse import quote_plus

import pymongo


class Config:
	TELEGRAM_TOKEN_BOT = os.getenv('TELEGRAM_TOKEN_BOT')
	MONGO_DB_URL = os.getenv('MONGO_DB_URL')

	def get_mongo_client(self):
		return pymongo.MongoClient(self.MONGO_DB_URL)


config = Config()
