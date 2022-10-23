import json

from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from bson.objectid import ObjectId

from mongo import MongoFieldsDB, MongoAnswersDB, MongoReadyFormsDB


async def check_form_need_merge(message: Message):
    fields_to_merge = []
    to_merge = []
    merged_fields = []
    fields = await MongoFieldsDB().find_all()
    merged_fields_q = await MongoReadyFormsDB().find_all()
    for field in merged_fields_q:
        merged_fields.append(field.get('field').get('_id'))

    for field in fields:
        if field.get('_id') not in merged_fields:
            fields_to_merge.append(field)

    if not fields_to_merge:
        await message.answer('В форме нет конфликтов!')
        return 0

    for field in fields_to_merge:
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
    if isinstance(message, Message):
        await message.answer(
            text="Есть нерешенные конфликты в форме. С помощью кнопок, решите их.",
            reply_markup=inline_kb_full,
        )
    else:
        await message.message.delete()
        await message.bot.send_message(
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
    field = await MongoFieldsDB().find_one({'_id': answer.get('to_field')})
    if isinstance(answer.get('answer'), list):
        answer_text = ' & '.join(answer.get('answer'))
    else:
        answer_text = answer.get('answer')
    text = f'Ответ от пользователя {answer.get("from")}.\n\n{answer_text} принят!'

    await MongoReadyFormsDB().insert_one(
        {
            "field": field,
            "answer": answer,
        }
    )

    await call_back.message.edit_text(
        text=text,
    )


async def ready_form(_):
    json = {'data': []}
    ready_answers = await MongoReadyFormsDB().find_all()
    for answer in ready_answers:
        field = answer.get('field')
        answer = answer.get('answer')
        json['data'].append(
            {
                'to_field_id': field.get('field_id'),
                'to_fild_name': field.get('field_name'),
                'field_type': field.get('field_type'),
                'answer_from': answer.get('from'),
                'answer': answer.get('answer')
            }
        )
    print(json)
    return json
