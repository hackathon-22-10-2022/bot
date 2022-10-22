from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.utils import markdown

from config import config
from forms import Form


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


async def question_message_sendler(question_number: int, message: Message) -> None:
	input_form_data = config.get_input_data()

	match input_form_data['data'][question_number]['field_type']:
		case 'text':
			await message.reply(
				markdown.text(
					markdown.hbold(f'Вопрос {question_number + 1}:'),
					markdown.hitalic(input_form_data['data'][question_number]['field_name']),
					markdown.text(input_form_data['data'][question_number]['field_description']),
					markdown.text(),
					markdown.text('Ответьте на вопрос:'),
					sep='\n'
				),
			)
		case 'checkbox':
			await message.reply(
				markdown.text(
					markdown.hbold(f'Вопрос {question_number + 1}:'),
					markdown.hitalic(input_form_data['data'][question_number]['field_name']),
					markdown.text(input_form_data['data'][question_number]['field_description']),
					markdown.text(),
					markdown.text('Выберите один или несколько вариантов:'),
					markdown.text(checkbox_field_values_to_str(input_form_data['data'][question_number]['field_values'])),
					sep='\n'
				),
			)
		case 'radiobox':
			await message.reply(
				markdown.text(
					markdown.hbold(f'Вопрос {question_number + 1}:'),
					markdown.hitalic(input_form_data['data'][question_number]['field_name']),
					markdown.text(input_form_data['data'][question_number]['field_description']),
					markdown.text(),
					markdown.text('Выберите один из вариантов:'),
					markdown.text(radio_field_values_to_str(input_form_data['data'][question_number]['field_values'])),
					sep='\n'
				),
			)
		case 'file':
			await message.reply(
				markdown.text(
					markdown.hbold(f'Вопрос {question_number + 1}:'),
					markdown.hitalic(input_form_data['data'][question_number]['field_name']),
					markdown.text(input_form_data['data'][question_number]['field_description']),
					markdown.text(),
					markdown.text('Отправьте файл'),
					sep='\n'
				),
			)


async def start_answering(message: Message, state: FSMContext):
	await Form.question1.set()
	await question_message_sendler(0, message)


async def answer1(message: Message, state: FSMContext):

	async with state.proxy() as data:
		data['answer1'] = message.text

	await Form.next()
	await question_message_sendler(1, message)



async def answer2(message: Message, state: FSMContext):

	async with state.proxy() as data:
		data['answer2'] = message.text

	await Form.next()
	await question_message_sendler(2, message)



async def answer3(message: Message, state: FSMContext):

	async with state.proxy() as data:
		data['answer3'] = message.text

	await Form.next()
	await question_message_sendler(3, message)



async def answer4(message: Message, state: FSMContext):

	async with state.proxy() as data:
		data['answer4'] = message.text

	await Form.next()
	await question_message_sendler(4, message)



async def answer5(message: Message, state: FSMContext):

	async with state.proxy() as data:
		data['answer5'] = message.text
	
	await state.finish()

	await message.answer('Спасибо за ответы! Вот они: ')
	await message.answer(data['answer1'])
	await message.answer(data['answer2'])
	await message.answer(data['answer3'])
	await message.answer(data['answer4'])
	await message.answer(data['answer5'])
	
	
