import requests
import telebot
from telebot import types
from SimpleQIWI import *



bot = telebot.TeleBot('123') # токен от бота в телеграм, создать бота можно тут - t.me/BotFather


number = '123' # номер киви
token = '321' # токен киви, взять тут - qiwi.com/api
api = QApi(token=token, phone=number)
sum = 100 # сколько мамонт должен заплатить



menu = types.InlineKeyboardMarkup(row_width=3)
menu.add(
	types.InlineKeyboardButton(text='Купить', callback_data='buy'),                       # +
	types.InlineKeyboardButton(text='Информация', callback_data='info')                      # +
)

games = types.InlineKeyboardMarkup(row_width=3)
games.add(
	types.InlineKeyboardButton(text='Pubg mobile', callback_data='pubg'),
	types.InlineKeyboardButton(text='Brawl Stars', callback_data='brawl'),
	types.InlineKeyboardButton(text='Standoff 2', callback_data='standoff'),
	types.InlineKeyboardButton(text='Назад', callback_data='back')
	)


@bot.message_handler(content_types=["text"])
def message_send(message):
	chat_id = message.chat.id
	message_id = message.message_id
	username = message.from_user.first_name

	starter= f'''
	Привет, {username}! Это бот для покупки валюты в разных играх.
	Нажимай на клавиатуру ниже..
	'''

	if message.text == '/start':
		bot.send_message(chat_id, starter, reply_markup=menu)


@bot.callback_query_handler(func=lambda call: True)
def handler_call(call):
	chat_id = call.message.chat.id
	message_id = call.message.message_id
	username = call.from_user.first_name
	oplata = 'opl' + str(chat_id)
	sendRequests = f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={number}&amountInteger={sum}&amountFraction=0&extra%5B%27comment%27%5D={oplata}&currency=643&blocked%5B0%5D=sum&blocked%5B1%5D=comment&blocked%5B2%5D=account"
	buy1 = types.InlineKeyboardMarkup(row_width=3)
	buy1.add(
		types.InlineKeyboardButton(text='Оплатить', url=sendRequests, callback_data='pay'),
		types.InlineKeyboardButton(text='Проверить оплату', callback_data='check'),
		types.InlineKeyboardButton(text='Назад', callback_data='back')
	)

	if call.data == 'buy':
		bot.send_message(chat_id, 'Выберите игру, для которой хотите купить валюту', reply_markup=games)
	elif call.data == 'info':
		helpp = '''
		Помощь

		Это бот для покупки валюты для таких игр как: Pubg mobile, Standoff 2, Brawl Start.

		Чтобы приобрести подписку на валюту, нажмите "Купить", после оплаты, администратор попросит у вас ваши игровые данные, чтобы отправить валюту.
		'''
		bot.send_message(chat_id, helpp, reply_markup=menu)
	elif call.data == 'brawl':
		bbb = 	f'''
		Приобретение валюты для Brawl Stars
		Стоимость бесконечной подписки на валюту: {sum}руб
		После оплаты, вы будете перенаправлены на получение валюты
		Ваш ID: {chat_id}
		'''

		bot.send_message(chat_id, bbb,  parse_mode='MarkdownV2', reply_markup=buy1)
	elif call.data == 'standoff':
		bbb = 	f'''
		Приобретение валюты для Standoff 2
		Стоимость бесконечной подписки на валюту: {sum}руб
		После оплаты, вы будете перенаправлены на получение валюты
		Ваш ID: {chat_id}
		'''

		bot.send_message(chat_id, bbb,  parse_mode='MarkdownV2', reply_markup=buy1)		


	elif call.data == 'pubg':
		bbb = 	f'''
		Приобретение валюты для Pubg Mobile
		Стоимость бесконечной подписки на валюту: {sum}руб
		После оплаты, вы будете перенаправлены на получение валюты
		Ваш ID: {chat_id}
		'''

		bot.send_message(chat_id, bbb,  parse_mode='MarkdownV2', reply_markup=buy1)
	elif call.data == 'check':
		try:
			payload = 'opl' + str(chat_id)
			bot.send_message(chat_id, 'Начинаю проверку платежей...')
			for i in range(len(api.payments['data'])):
				if api.payments['data'][i]['comment'] == payload and api.payments['data'][i]['sum']['amount'] == sum:
					bot.send_message(chat_id, 'Что-то пошло не по плану, подождите немного...', reply_markup=menu)

			bot.send_message(chat_id, 'Ошибка: Не найдено', reply_markup=buy1)
		except:
			print('11122')

	elif call.data == 'back':
		starter= f'''
		Привет, {username}! Это бот для покупки валюты в разных играх.
		Нажимай на клавиатуру ниже..
		'''
		bot.send_message(chat_id, starter, reply_markup=menu)

bot.polling(none_stop=True)