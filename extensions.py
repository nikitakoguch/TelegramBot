import requests
import json
from config import keys


class APIException(Exception):
    pass

class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        
        if quote == base:
            raise APIException('Выберите, пожалуйста, разные валюты')
    
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обрабоать валюту {quote}\nДля просмотра доступных волют\
воспользуйтесь командой /values')
    
        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}\nДля просмотра доступных волют\
воспользуйтесь командой /values')
    
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}\nЗначение воодится цифрами!В случае\
необходимости конвертировать не целостное число\nИспользуйте точку\nПример:50.73')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        result = total_base * int(amount)
        return result