from aiogram.dispatcher.filters.state import State, StatesGroup


class FormAllQuestions(StatesGroup):
    question1 = State()
    question2 = State()
    question3 = State()
    question4 = State()
    question5 = State()


class FormOneQuestion(StatesGroup):
    question_number = State()
    question_answer = State()
