import requests
import json
import os

response = requests.get('https://raw.githubusercontent.com/nelsoneltz/stock_api/master/sample.json')

print(response.json())

# print(os.path.dirname(__file__))
# os.path.dirname()
