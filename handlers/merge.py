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

    await message.answer(
        text="Есть нерешенные конфликты в форме. С помощью кнопок, решите их.",
        reply_markup=inline_kb_full,
    )


async def show_problems_in_field(call_back: CallbackQuery):
    field_id = int(call_back.data.split(":")[-1])
    print(field_id)
    field = await MongoFieldsDB().get_by_field_number(field_id)

    answers = await MongoAnswersDB().find_many({"to_field": field.get("_id")})
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    was = []
    for answer in answers:
        if answer.get("answer") not in was:
            print(answer)
            was.append(answer.get("answer"))
            text = answer.get("answer")  # todo рекогнайз из id в текст
            if isinstance(answer.get("answer"), list):
                text = "&".join(answer.get("answer"))

            inline_kb_full.add(
                InlineKeyboardButton(
                    text=text, callback_data=f'choose:{answer.get("_id")}'
                )
            )

    await call_back.message.edit_text(
        text=f'Выберете нужный вариант ответа для поля: {field.get("field_name")}',
        reply_markup=inline_kb_full,
    )
