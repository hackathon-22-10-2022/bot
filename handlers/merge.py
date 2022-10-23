import json

from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)

from mongo import MongoFieldsDB, MongoAnswersDB


async def check_form_need_merge(message: Message):
    to_merge = []
    fields = await MongoFieldsDB().find_all()
    for field in fields:

        answers = await MongoAnswersDB().find_many({"to_field": field.get("_id")})

        if len(answers) != 1:
            to_merge.append(
                {
                    "field_name": field.get("field_name"),
                    "field_id": field.get("_id"),
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

    await message.answer(
        text="Есть нерешенные конфликты в форме. С помощью кнопок, решите их.",
        reply_markup=inline_kb_full,
    )


async def show_problems_in_field(callback_query: CallbackQuery):
    field_id = callback_query.data.split(":")
    answers = await MongoAnswersDB().find_many({"to_field": field_id})
    for answer in answers:
        print(answer)
