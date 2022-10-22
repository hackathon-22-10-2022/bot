from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown

from config import config
from forms import Form
from mongo import MongoAnswersDB, MongoFieldsDB


def checkbox_field_values_to_str(field_values: dict) -> str:
	str = ''
	for key, value in field_values.items():
		str += f'{key}: {value}\n'
	return str[:-1]


def radio_field_values_to_str(field_values: list) -> str:
	str = ''
	i = 1
	for value in field_values:
		str += f'{i}: {value}\n'
		i += 1
	return str[:-1]


async def _question_message_sendler(question_number: int, message: Message) -> None:
	input_form_data = await MongoFieldsDB().find_all()

	match input_form_data[question_number]['field_type']:
		case 'text':
			await message.reply(
				markdown.text(
					markdown.hbold(f'Вопрос {question_number + 1}:'),
					markdown.hitalic(input_form_data[question_number]['field_name']),
					markdown.text(input_form_data[question_number]['field_description']),
					markdown.text(),
					markdown.text('Ответьте на вопрос:'),
					sep='\n'
				),
			)
		case 'checkbox':
			await message.reply(
				markdown.text(
					markdown.hbold(f'Вопрос {question_number + 1}:'),
					markdown.hitalic(input_form_data[question_number]['field_name']),
					markdown.text(input_form_data[question_number]['field_description']),
					markdown.text(),
					markdown.text('Выберите один или несколько вариантов (через запятую):'),
					markdown.text(checkbox_field_values_to_str(input_form_data[question_number]['field_values'])),
					sep='\n'
				),
			)
		case 'radiobox':
			await message.reply(
				markdown.text(
					markdown.hbold(f'Вопрос {question_number + 1}:'),
					markdown.hitalic(input_form_data[question_number]['field_name']),
					markdown.text(input_form_data[question_number]['field_description']),
					markdown.text(),
					markdown.text('Выберите один из вариантов:'),
					markdown.text(radio_field_values_to_str(input_form_data[question_number]['field_values'])),
					sep='\n'
				),
			)
		case 'file':
			await message.reply(
				markdown.text(
					markdown.hbold(f'Вопрос {question_number + 1}:'),
					markdown.hitalic(input_form_data[question_number]['field_name']),
					markdown.text(input_form_data[question_number]['field_description']),
					markdown.text(),
					markdown.text('Отправьте файл'),
					sep='\n'
				),
			)


async def start_answering(message: Message, state: FSMContext):
	await Form.question1.set()
	await _question_message_sendler(0, message)


async def _answer_generator(state_name: str, state_number: int, state: FSMContext, message: Message):
	async with state.proxy() as data:
		data[state_name] = message.text
	
	mongo_field = await MongoFieldsDB().find_all()
	await MongoAnswersDB().insert_answer(mongo_field[state_number]['_id'], message.from_user.id, data[state_name])

	# answer = data['answer1']
	# if mongo_field[0]['field_type'] == 'checkbox':
	# 	answer = map(int, data['answer1'].split(', '))
	if state_number == 4:
		await state.finish()
		await message.answer('Спасибо за ответы! Вот они: ')
		await message.answer(data['answer1'])
		await message.answer(data['answer2'])
		await message.answer(data['answer3'])
		await message.answer(data['answer4'])
		await message.answer(data['answer5'])	
		return 

	await Form.next()
	await _question_message_sendler(state_number + 1, message)


async def answer1(message: Message, state: FSMContext):
	await _answer_generator('answer1', 0, state, message)
	

async def answer2(message: Message, state: FSMContext):
	await _answer_generator('answer2', 1, state, message)


async def answer3(message: Message, state: FSMContext):
	await _answer_generator('answer3', 2, state, message)



async def answer4(message: Message, state: FSMContext):
	await _answer_generator('answer4', 3, state, message)


async def answer5(message: Message, state: FSMContext):
	await _answer_generator('answer5', 4, state, message)


	

	
