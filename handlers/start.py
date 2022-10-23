from aiogram.types import Message
from aiogram.utils import markdown


async def start(message: Message):
    await

    await message.answer(
        markdown.text(
                markdown.hbold("Добро пожаловать! 👋"),
                markdown.text("Это бот для сбора данных через формы."),
                markdown.text("Для начала работы введите команду: /start_answering"),
                sep="\n"
            )
    )
