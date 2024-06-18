import requests
import json
from config import keys


class APIException(Exception):
	pass


class Convertor:
	@staticmethod
	def get_price(quote: str, base: str, amount: str):
		quote, base, amount = list(map(lambda x: str.lower(x), [quote, base, amount]))

		if quote == base:
			raise APIException(f'Невозможно перевести одинаковые валюты {base}')

		try:
			quote_ticker = keys[quote]
		except KeyError:
			raise APIException(f'Не удалось обработать валюту {quote}')

		try:
			base_ticker = keys[base]
		except KeyError:
			raise APIException(f'Не удалось обработать валюту {base}')

		try:
			amount = float(amount)
		except ValueError:
			raise APIException(f'Не удалось обработать количество {amount}')

		data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
		value_quote = json.loads(data.content)['Valute'][quote_ticker]['Value'] if quote_ticker != 'RUB' else 1
		value_base = json.loads(data.content)['Valute'][base_ticker]['Value'] if base_ticker != 'RUB' else 1

		total_base = value_quote / value_base * amount

		return total_base
