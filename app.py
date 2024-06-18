import telebot
from config import keys, TOKEN
from extensions import APIException, Convertor

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def echo_test(message: telebot.types.Message):
	text = 'Для начала работы введите команду в следюущем формате:\n<имя валюты> ' \
		   '<в какую валюту перевести> ' \
		   '<количество переводимой валюты>\nЧтобы увидеть список доступных валют, введите /values\n' \
		   'Бот нечувствителен к регистру, но не совершайте орфографических ошибок'
	bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
	text = 'Доступные валюты:'
	for key in keys:
		text = '\n'.join((text, key))
	bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
	if message.text[0] == '/':
		bot.reply_to(message, 'Неизвестная команда')
	else:
		try:
			values = message.text.split(' ')

			if len(values) != 3:
				raise APIException('Не корректное число параметров')

			quote, base, amount = values
			total_base = Convertor.get_price(quote, base, amount)
		except APIException as e:
			bot.reply_to(message, f'Ошибка пользователя\n{e}')
		except Exception as e:
			bot.reply_to(message, f'Не удалось обработать команду\n{e}')
		else:
			text = f'Цена {amount} {quote} в {base} - {round(total_base, 4)}'
			bot.send_message(message.chat.id, text)


bot.polling()
