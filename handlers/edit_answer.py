from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from aiogram.utils import markdown

from forms import FormOneQuestion
from handlers.answer import get_all_user_answers_to_message
from keyboards.edit_after_send_answers import edit_after_send_answers
from mongo import MongoFieldsDB, MongoAnswersDB


async def _edit_handler(callback_query: types.CallbackQuery, question_number: int, state: FSMContext):
    await FormOneQuestion.question_number.set()
    async with state.proxy() as data:
        data['question_number'] = question_number

    field = await MongoFieldsDB().get_by_field_number(question_number)

    match field["field_type"]:
        case "text":
            ask = markdown.text("Ответьте на вопрос:")
        case "checkbox":
            ask = markdown.text("Выберите один или несколько вариантов (через запятую):")
        case "radiobox":
            ask = markdown.text("Выберите один вариант:")
        case "file":
            ask = markdown.text("Отправьте файл:")
        case _:
            ask = markdown.text("Ответьте на вопрос:")

    await callback_query.message.answer(
        markdown.text(
            markdown.hbold(f"Вопрос {question_number}:"),
            markdown.hitalic(field["field_name"]),
            markdown.text(field["field_description"]),
            markdown.text(),
            ask,
            sep="\n",
        ),
    )
    await FormOneQuestion.next()


async def edit1(callback_query: types.CallbackQuery, state: FSMContext):
    await _edit_handler(callback_query, 1, state)


async def edit2(callback_query: types.CallbackQuery, state: FSMContext):
    await _edit_handler(callback_query, 2, state)


async def edit3(callback_query: types.CallbackQuery, state: FSMContext):
    await _edit_handler(callback_query, 3, state)


async def edit4(callback_query: types.CallbackQuery, state: FSMContext):
    await _edit_handler(callback_query, 4, state)


async def edit5(callback_query: types.CallbackQuery, state: FSMContext):
    await _edit_handler(callback_query, 5, state)


async def edit_answer(message: Message, state: FSMContext):
    mongo_field = await MongoFieldsDB().find_all()

    async with state.proxy() as data:
        await MongoAnswersDB().update_one({
            'to_field': mongo_field[data['question_number'] - 1]["_id"],
            'from': message.from_user.id
        },
            {"$set": {'answer': message.text}}
        )

    await state.finish()
    await message.answer(
        await get_all_user_answers_to_message(message.from_user.id),
        reply_markup=edit_after_send_answers(),
    )


