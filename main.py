import asyncio

from config import config, mongo_config


	
async def do_insert():
    document = {'name': '1234567890'}
    result = await mongo_config.get_mongo_collection().insert_one(document)
    print('result %s' % repr(result.inserted_id))


loop = mongo_config.get_mongo_client().get_io_loop()
print(mongo_config.get_mongo_client())
loop.run_until_complete(do_insert())





