import requests
import json
from data.sectors import sectors
from data.request_params import cookies, headers, params

def get_list(d, col):
    i = 0
    n = col
    list_symbol = []
    while True:
        data = d
        d["size"] = n
        d["offset"] = i*n
        response = requests.post('https://query1.finance.yahoo.com/v1/finance/screener', params=params, cookies=cookies, headers=headers, json=data)
        r = response.text
        if json.loads(r)["finance"]["result"][0]["quotes"] != []:
            for item in json.loads(r)["finance"]["result"][0]["quotes"]:
                list_symbol.append(item["symbol"])
        else:
            break
        i += 1
    return list_symbol
