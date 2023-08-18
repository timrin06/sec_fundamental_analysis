from ttgi import keys
import requests
import json
from data.request_params import cookies, headers, params
aapl_cik = "0000320193"
l = []
for i in keys:
    try:
        json.loads(requests.get("https://data.sec.gov/api/xbrl/frames/us-gaap/"+ i +"/USD/CY2022Q1I.json", cookies=cookies, headers=headers).text)["data"]
        l.append(i)
    except json.decoder.JSONDecodeError:
        pass
print(l)
print(list(keys.keys()))
