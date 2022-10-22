import asyncio
import json
from typing import Type

from mongo import MongoUsersDB, MongoFieldsDB, AbstarctMongoDB


async def init_json_to_mongo(connection: Type[AbstarctMongoDB], data: dict | list):
    if isinstance(data, list):
        for d in data:
            print(await connection().insert_one(d))
    
    if isinstance(data, dict):
        print(await connection().insert_one(data))


async def init_db():
    with open('input_data.json') as f:
        data = json.load(f)
        fileds_connection = MongoFieldsDB
        users_connection = MongoUsersDB
        
        await init_json_to_mongo(fileds_connection, data["data"])
        await init_json_to_mongo(users_connection, data["users"])


asyncio.run(init_db())
