import asyncio

from config import config, mongo_config


	
async def do_insert():
    document = {'name2': '1234567890222'}
    result = await mongo_config.get_mongo_collection().insert_one(document)
    print('result %s' % repr(result.inserted_id))


asyncio.run(do_insert())


