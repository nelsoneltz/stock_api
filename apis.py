import requests
from key import API_KEY
import datetime
from abc import ABC, abstractmethod
import logging
import json
import os



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class AlphaVantage(ABC):

    def __init__(self,symbol:str) -> None:
        self.symbol = symbol
        self.base_endpoint = f"https://www.alphavantage.co/query?apikey={API_KEY}"

    @abstractmethod
    def _get_endpoint(self) -> str:
        pass

    def get_data(self,**kwargs) -> dict:
        endpoint = self._get_endpoint(**kwargs)
        logger.info(f"Getting data from endpoint: {endpoint}")
        response = requests.get(endpoint)
        response.raise_for_status()
        return response.json()
    
class TimeSeriesDaily(AlphaVantage):
    type = 'TIME_SERIES_DAILY'

    def _get_endpoint(self) -> str:
        return f"{self.base_endpoint}&function={self.type}&symbol={self.symbol}"
    

class TimeSeriesMonthly(AlphaVantage):
    type = 'TIME_SERIES_MONTHLY'

    def _get_endpoint(self) -> str:
        return f"{self.base_endpoint}&function={self.type}&symbol={self.symbol}"

class TimeSeriesIntraday(AlphaVantage):
    type = 'TIME_SERIES_INTRADAY'

    def _get_endpoint(self,interval:str) -> str:
        return f"{self.base_endpoint}&function={self.type}&symbol={self.symbol}&interval={interval}"

teste = TimeSeriesDaily(symbol = 'IBM')

with open('checkpoint.txt','r') as f:
    checkpoint = f.read()

dicionario = teste.get_data()
print(dicionario)

last_refreshed_date = dicionario['Meta Data']['3. Last Refreshed']
print(last_refreshed_date)

if last_refreshed_date == checkpoint:
    print("Dado mais atualizado. Até amanhã.")
else:
    with open('checkpoint.txt','w') as f:
        f.write(last_refreshed_date)

    exist_ = os.path.exists('arquivos')
    if not exist_:
        os.makedirs('arquivos', exist_ok=True)
    with open(f'arquivos/{last_refreshed_date}_{teste.symbol}.json','w') as f2:
        json.dump(dicionario['Time Series (Daily)'][last_refreshed_date],f2)

