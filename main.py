import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from handlers import start, answer, merge, edit_answer
from config import config
from forms import FormAllQuestions, FormOneQuestion
from merger.checkboxs import merge_checkboxes
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

dp.register_message_handler(
    answer.answer1, state=FormAllQuestions.question1, content_types=["photo", "text"]
)
dp.register_message_handler(
    answer.answer2, state=FormAllQuestions.question2, content_types=["photo", "text"]
)
dp.register_message_handler(
    answer.answer3, state=FormAllQuestions.question3, content_types=["photo", "text"]
)
dp.register_message_handler(
    answer.answer4, state=FormAllQuestions.question4, content_types=["photo", "text"]
)
dp.register_message_handler(
    answer.answer5, state=FormAllQuestions.question5, content_types=["photo", "text"]
)

dp.register_callback_query_handler(
    edit_answer.edit1, lambda c: c.data == "edit_after_send_answers-1"
)
dp.register_callback_query_handler(
    edit_answer.edit2, lambda c: c.data == "edit_after_send_answers-2"
)
dp.register_callback_query_handler(
    edit_answer.edit3, lambda c: c.data == "edit_after_send_answers-3"
)
dp.register_callback_query_handler(
    edit_answer.edit4, lambda c: c.data == "edit_after_send_answers-4"
)
dp.register_callback_query_handler(
    edit_answer.edit5, lambda c: c.data == "edit_after_send_answers-5"
)

dp.register_message_handler(
    edit_answer.edit_answer,
    state=FormOneQuestion.question_answer,
    content_types=["photo", "text"],
)

dp.register_message_handler(merge.check_form_need_merge, commands=["merge"])
dp.register_callback_query_handler(
    merge.check_form_need_merge, lambda c: c.data == "check_need_merge"
)
dp.register_callback_query_handler(
    merge.show_problems_in_field, lambda c: c.data.startswith("merge")
)
dp.register_callback_query_handler(
    merge.view_version, lambda c: c.data.startswith("choose:")
)
dp.register_callback_query_handler(
    merge.accept_answer, lambda c: c.data.startswith("accept_answer")
)
dp.register_message_handler(merge.ready_form, commands=["ready_form"])
dp.register_message_handler(merge_checkboxes, commands=["test"])
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


# TODO: ?????? ???????????? ???????????? ???????????????????? ??????????, ???????????? ???????????????? ???? ???????? `from` ?? ???????????? answer.
#       ???????? ?????? ???? `senders` ?????????????????? ??????????, ???? ???????????????????? ?????????????????? `foremans` ?????? ????????,
#       ?????????? ?????? ?????????????? ?????????????? ????????????????????.
