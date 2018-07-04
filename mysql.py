import requests
import json

headers = {'Content-Type': 'application/json', 'Accept':'application/json'}

ticker = [{"security":"ARM","price":13.4,"price_change":0.2},{"security":"BAMB","price":170,"price_change":0}]

payload = {
    "ticker": ticker
    }
data = json.dumps(ticker)

r = requests.get("https://onlinetrading.nse.co.ke/tradeweb111/handler/fh.ashx?"
                 "query=javascript"
                 "&output=json"
                 "&tp=0"
                 "&id=karis"
                 "&mdf=1"
                 "&iid=51"
                 "&sky=bb67fced8b1b"
                 "&sc=3"
                 "&callback=xdrCall.JsonXSHR"
                 "&nocache=1530640166427")

print(r.text)