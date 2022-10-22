from aiogram.dispatcher.filters.state import State, StatesGroup


class Form(StatesGroup):
	question1 = State()
	question2 = State()
	question3 = State()
	question4 = State()
	question5 = State()
