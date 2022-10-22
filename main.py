import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram_dialog import Window, Dialog, DialogRegistry
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from handlers import start
from config import config
from forms.states import MySG

storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_TOKEN_BOT)
dp = Dispatcher(bot, storage=storage)
registry = DialogRegistry(dp)

logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s %(levelname)s - %(module)s - %(funcName)s - %(lineno)d: %(message)s",
	datefmt='%H:%M:%S %d.%m.%Y',
)


main_window = Window(
    Const("Hello, unknown person"),
    Button(Const("Useless button"), id="nothing"),
    state=MySG.main,
)

dialog = Dialog(main_window)
registry.register(dialog)

dp.register_message_handler(start.start, commands=['start'])



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
