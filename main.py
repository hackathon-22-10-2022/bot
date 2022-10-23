import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import start, answer
from config import config
from forms import Form
from middleware import WhileListUsersMiddleware

storage = MemoryStorage()
bot = Bot(token=config.TELEGRAM_TOKEN_BOT, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s - %(module)s - %(funcName)s - %(lineno)d: %(message)s",
    datefmt="%H:%M:%S %d.%m.%Y",
)

dp.middleware.setup(WhileListUsersMiddleware())

dp.register_message_handler(start.start, commands=["start"])
dp.register_message_handler(answer.start_answering, commands=["start_answering"])
dp.register_message_handler(answer.answer1, state=Form.question1, content_types=['photo', 'text'])
dp.register_message_handler(answer.answer2, state=Form.question2, content_types=['photo', 'text'])
dp.register_message_handler(answer.answer3, state=Form.question3, content_types=['photo', 'text'])
dp.register_message_handler(answer.answer4, state=Form.question4, content_types=['photo', 'text'])
dp.register_message_handler(answer.answer5, state=Form.question5, content_types=['photo', 'text'])

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


# TODO: при каждом полном заполнении формы, делать итерацию по всем `from` в модели answer.
#       Если все из `senders` заполнили форму, то отправлять сообщение `foremans` для того,
#       чтобы они сделали решение конфликтов.
# TODO: сделать механизм решения конфликтов
# TODO: генерировать выходной json по типу, который был предоставлен
