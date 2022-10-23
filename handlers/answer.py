from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown

from config import config
from keyboards.edit_after_send_answers import edit_after_send_answers
from utils import (
    convert_str_with_commas_to_list,
    checkbox_field_values_to_str,
    radio_field_values_to_str,
)
from forms import FormAllQuestions
from mongo import MongoAnswersDB, MongoFieldsDB


async def _question_message_sendler(question_number: int, message: Message) -> None:
    input_form_data = await MongoFieldsDB().find_all()

    match input_form_data[question_number]["field_type"]:
        case "text":
            await message.reply(
                markdown.text(
                    markdown.hbold(f"Вопрос {question_number + 1}:"),
                    markdown.hitalic(input_form_data[question_number]["field_name"]),
                    markdown.text(
                        input_form_data[question_number]["field_description"]
                    ),
                    markdown.text(),
                    markdown.text("Ответьте на вопрос:"),
                    sep="\n",
                ),
            )
        case "checkbox":
            await message.reply(
                markdown.text(
                    markdown.hbold(f"Вопрос {question_number + 1}:"),
                    markdown.hitalic(input_form_data[question_number]["field_name"]),
                    markdown.text(
                        input_form_data[question_number]["field_description"]
                    ),
                    markdown.text(),
                    markdown.text(
                        "Выберите один или несколько вариантов (через запятую):"
                    ),
                    markdown.text(
                        checkbox_field_values_to_str(
                            input_form_data[question_number]["field_values"]
                        )
                    ),
                    sep="\n",
                ),
            )
        case "radiobox":
            await message.reply(
                markdown.text(
                    markdown.hbold(f"Вопрос {question_number + 1}:"),
                    markdown.hitalic(input_form_data[question_number]["field_name"]),
                    markdown.text(
                        input_form_data[question_number]["field_description"]
                    ),
                    markdown.text(),
                    markdown.text("Выберите один из вариантов:"),
                    markdown.text(
                        radio_field_values_to_str(
                            input_form_data[question_number]["field_values"]
                        )
                    ),
                    sep="\n",
                ),
            )
        case "file":
            await message.reply(
                markdown.text(
                    markdown.hbold(f"Вопрос {question_number + 1}:"),
                    markdown.hitalic(input_form_data[question_number]["field_name"]),
                    markdown.text(
                        input_form_data[question_number]["field_description"]
                    ),
                    markdown.text(),
                    markdown.text("Отправьте файл"),
                    sep="\n",
                ),
            )


async def get_all_user_answers_to_message(user_id: int) -> str:
    user_answers = await MongoAnswersDB().get_user_answers(user_id)
    message_to_send = ""
    for user_answer in user_answers:
        field = await MongoFieldsDB().get_by_field_id(user_answer["to_field"])

        message_to_send += (
            markdown.text(
                markdown.hbold(f"Вопрос {field['field_id']}:"),
                markdown.hitalic(field["field_name"]),
                markdown.text(field["field_description"]),
                markdown.text(),
                markdown.text("Ваш ответ:"),
                markdown.text(user_answer["answer"]),
                sep="\n",
            )
            + "\n" * 2
        )

    return message_to_send


async def start_answering(message: Message, state: FSMContext):
    user_answers = await MongoAnswersDB().get_user_answers(message.from_user.id)
    if len(user_answers) > 0:
        await message.answer(
            "Вы уже заполнили форму. Вы можете её изменить. Ваши ответы будут перезаписаны."
        )
        await message.answer(
            await get_all_user_answers_to_message(message.from_user.id),
            reply_markup=edit_after_send_answers(),
        )
        return

    await FormAllQuestions.question1.set()
    await _question_message_sendler(0, message)


async def _answer_validation(field_type: str, field_values: dict, answer: str) -> bool:
    match field_type:
        case "text" | "file":
            return True

        case "checkbox":
            answer = convert_str_with_commas_to_list(answer)
            if len(answer) == 0:
                return False
            for a in answer:
                if str(a) not in field_values.keys():
                    return False
            return True

        case "radiobox":
            try:
                answer = int(answer)
            except ValueError:
                return False
            if answer not in list(range(1, len(field_values) + 1)):
                return False
            return True


async def _answer_generator(
    state_name: str, state_number: int, state: FSMContext, message: Message
):
    async with state.proxy() as data:
        data[state_name] = message.text

    mongo_field = await MongoFieldsDB().find_all()

    if mongo_field[state_number]["field_type"] == "file":
        if len(message.photo) == 0:
            await message.reply("Отправьте фотографию!")
            return

        path_to_file = f"{config.BASE_DIR}/{config.PATH_TO_USERS_FILE_FOLDER}/{state_number}_{message.from_user.id}.jpg"
        await message.photo[-1].download(destination_file=path_to_file)
        async with state.proxy() as data:
            data[state_name] = path_to_file
        await MongoAnswersDB().insert_answer(
            mongo_field[state_number]["_id"], message.from_user.id, path_to_file
        )
        await FormAllQuestions.next()
        await _question_message_sendler(state_number + 1, message)
        return
    elif len(message.photo) > 0:
        await message.reply("Отправьте только текст!")
        return

    if mongo_field[state_number]["field_type"] not in ["text", "file"]:
        if not await _answer_validation(
            mongo_field[state_number]["field_type"],
            mongo_field[state_number]["field_values"],
            data[state_name],
        ):
            await message.reply("Попробуйте ввести ответ ещё раз!")
            return

    answer = data[state_name]
    match mongo_field[state_number]["field_type"]:
        case "checkbox":
            answer = convert_str_with_commas_to_list(answer)
        case "radiobox":
            answer = int(answer)

    await MongoAnswersDB().insert_answer(
        mongo_field[state_number]["_id"], message.from_user.id, answer
    )

    if state_number == 4:
        await state.finish()
        await message.answer("Спасибо за ответы! Вот они: ")
        await message.answer(
            await get_all_user_answers_to_message(message.from_user.id)
        )
        return

    await FormAllQuestions.next()
    await _question_message_sendler(state_number + 1, message)


async def answer1(message: Message, state: FSMContext):
    await _answer_generator("answer1", 0, state, message)


async def answer2(message: Message, state: FSMContext):
    await _answer_generator("answer2", 1, state, message)


async def answer3(message: Message, state: FSMContext):
    await _answer_generator("answer3", 2, state, message)


async def answer4(message: Message, state: FSMContext):
    await _answer_generator("answer4", 3, state, message)


async def answer5(message: Message, state: FSMContext):
    await _answer_generator("answer5", 4, state, message)
