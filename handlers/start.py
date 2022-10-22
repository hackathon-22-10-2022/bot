from forms.states import MySG
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode


async def start(m: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MySG.main, mode=StartMode.RESET_STACK)

