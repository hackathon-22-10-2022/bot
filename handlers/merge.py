import json

from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from bson.objectid import ObjectId

from mongo import MongoFieldsDB, MongoAnswersDB


async def check_form_need_merge(message_or_callback: Message | CallbackQuery):
    to_merge = []
    fields = await MongoFieldsDB().find_all()
    for field in fields:

        answers = await MongoAnswersDB().find_many({"to_field": field.get("_id")})

        if len(answers) > 1:
            to_merge.append(
                {
                    "field_name": field.get("field_name"),
                    "field_id": field.get("field_id"),
                    "answers_count": len(answers),
                }
            )

    inline_kb_full = InlineKeyboardMarkup(row_width=2)

    for field in to_merge:
        callback_data = f'merge:{field.get("field_id")}'
        field_name = f'{field.get("field_name")} | {field.get("answers_count")}'
        inline_kb_full.add(
            InlineKeyboardButton(field_name, callback_data=callback_data)
        )
    if isinstance(message_or_callback, Message):
        await message_or_callback.answer(
            text="Есть нерешенные конфликты в форме. С помощью кнопок, решите их.",
            reply_markup=inline_kb_full,
        )
    else:
        await message_or_callback.message.delete()
        await message_or_callback.message.answer(
            text="Есть нерешенные конфликты в форме. С помощью кнопок, решите их.",
            reply_markup=inline_kb_full,
        )


async def show_problems_in_field(call_back: CallbackQuery):
    field_id = int(call_back.data.split(":")[-1])
    print(field_id)
    field = await MongoFieldsDB().get_by_field_number(field_id)

    answers = await MongoAnswersDB().find_many({"to_field": field.get('_id')})
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    was = []
    for answer in answers:
        if answer.get('answer') not in was:
            was.append(answer.get('answer'))  # todo распознавать был ли текст до этого или нет
            text = f'Данные от {answer.get("from")}'  # todo рекогнайз из id в текст в юзернейм

            inline_kb_full.add(
                InlineKeyboardButton(text=text, callback_data=f'choose:{answer.get("_id")}')
            )

    inline_kb_full.add(
        InlineKeyboardButton(text='◀️ Назад', callback_data='check_need_merge')
    )
    await call_back.message.edit_text(
        text=f'Выберете нужный вариант ответа для поля: {field.get("field_name")}',
        reply_markup=inline_kb_full
    )


async def view_version(call_back: CallbackQuery):
    answer_id = call_back.data.split(':')[-1]
    answer = await MongoAnswersDB().find_one({'_id': ObjectId(answer_id)})
    is_photo = False
    path_to_photo = None
    text = None
    if isinstance(answer.get('answer'), list):
        answer_text = ' & '.join(answer.get('answer'))
        text = f'Ответ от пользователя {answer.get("from")}.\n\n{answer_text}'

    elif '/' in str(answer.get('answer')):
        is_photo = True
        path_to_photo = answer.get('answer')
    else:
        answer_text = answer.get('answer')
        text = f'Ответ от пользователя {answer.get("from")}.\n\n{answer_text}'

    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    inline_kb_full.add(
        InlineKeyboardButton(text='Принять', callback_data=f'accept_answer:{answer_id}')
    )
    inline_kb_full.add(
        InlineKeyboardButton(text='◀️ Назад', callback_data=f'check_need_merge')
    )
    if is_photo:
        await call_back.message.delete()

        if path_to_photo:
            with open(path_to_photo, "rb") as f:
                await call_back.message.answer_photo(
                    photo=f,
                    caption=f'Фото от {answer.get("from")}',
                    reply_markup=inline_kb_full
                )

    else:
        if text:
            await call_back.message.edit_text(
                text=text,
                reply_markup=inline_kb_full
            )


async def accept_answer(call_back: CallbackQuery):
    answer_id = call_back.data.split(':')[-1]
    answer = await MongoAnswersDB().find_one({'_id': ObjectId(answer_id)})
    if isinstance(answer.get('answer'), list):
        answer_text = ' & '.join(answer.get('answer'))
    else:
        answer_text = answer.get('answer')
    text = f'Ответ от пользователя {answer.get("from")}.\n\n{answer_text} принят!'
