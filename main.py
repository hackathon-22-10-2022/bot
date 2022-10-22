import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import start
from config import config

storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)


logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s %(levelname)s - %(module)s - %(funcName)s - %(lineno)d: %(message)s",
	datefmt='%H:%M:%S %d.%m.%Y',
)


dp.register_message_handler(start.start, commands=['start'])



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

