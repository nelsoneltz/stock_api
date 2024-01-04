import requests
from key import API_KEY
import datetime
from abc import ABC, abstractmethod
import logging
import json

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

    def _get_endpoint(self,interval:str):
        return f"{self.base_endpoint}&function={self.type}&symbol={self.symbol}&interval={interval}"

teste = TimeSeriesIntraday(symbol = 'IBM')
# print(teste._get_endpoint())
# print(teste.get_data(interval='60min'))

# Serializing json
json_object = json.dumps(teste.get_data(interval='60min'), indent=4)
 
# Writing to sample.json
with open("sample.json", "w") as outfile:
    outfile.write(json_object)