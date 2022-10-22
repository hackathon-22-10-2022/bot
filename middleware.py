from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.utils import markdown

from mongo import MongoUsersDB


class WhileListUsersMiddleware(BaseMiddleware):

    async def on_process_message(
        self, message: types.Message, *args, **kwargs
    ):
        senders = await MongoUsersDB().get_senders()
        foremans = await MongoUsersDB().get_foremans()
        if message.from_user.id not in (senders | foremans):
            await message.answer(
                markdown.text(
                    markdown.hbold('Вы не авторизованы!'),
                    markdown.text('Для трудоустройства обратитесь на сайт: https://www.spetsdor.ru/'),
                    sep='\n'
                )
            )
            raise CancelHandler()

