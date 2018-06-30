import requests
import json

headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

ticker = [{"security":"ARM","price":13.4,"price_change":0.2},{"security":"BAMB","price":170,"price_change":0}]

payload = {
    "ticker": ticker
    }

r = requests.post("http://localhost/ooza/public_html/postTickerData", data=json.dumps(ticker))

print(r)