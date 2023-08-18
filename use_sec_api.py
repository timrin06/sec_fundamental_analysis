import requests
import json
from data.sectors import sectors
from data.request_params import cookies, headers, params
from data.dannse import ciks
from get_list import get_list
import numpy as np
import pandas as pd

symbol_list = get_list({"size":25,"offset":0,"sortField":"intradaymarketcap","sortType":"DESC","quoteType":"EQUITY","topOperator":"AND","query":{"operator":"AND","operands":[{"operator":"or","operands":[{"operator":"EQ","operands":["region","us"]}]},{"operator":"or","operands":[{"operator":"GT","operands":["intradaymarketcap",100000000000]},{"operator":"BTWN","operands":["intradaymarketcap",10000000000,100000000000]},{"operator":"BTWN","operands":["intradaymarketcap",2000000000,10000000000]}]},{"operator":"gt","operands":["intradayprice",0]},{"operator":"or","operands":[{"operator":"EQ","operands":["sector","Healthcare"]}]},{"operator":"or","operands":[{"operator":"EQ","operands":["industry","Biotechnology"]}]},{"operator":"or","operands":[{"operator":"EQ","operands":["exchange","NAS"]},{"operator":"EQ","operands":["exchange","NYQ"]},{"operator":"EQ","operands":["exchange","YHD"]},{"operator":"EQ","operands":["exchange","NGM"]},{"operator":"EQ","operands":["exchange","NMS"]},{"operator":"EQ","operands":["exchange","NCM"]},{"operator":"EQ","operands":["exchange","BSE"]}]},{"operator":"or","operands":[{"operator":"EQ","operands":["exchange","NMS"]}]},{"operator":"gt","operands":["lastclosepricebookvalue.lasttwelvemonths",0]},{"operator":"gt","operands":["lastclosepricetangiblebookvalue.lasttwelvemonths",0]},{"operator":"gt","operands":["totalassets.lasttwelvemonths",0]},{"operator":"gt","operands":["totalcurrentassets.lasttwelvemonths",0]},{"operator":"gt","operands":["grossprofit.lasttwelvemonths",0]},{"operator":"gt","operands":["lastclosemarketcaptotalrevenue.lasttwelvemonths",0]}]},"userId":"","userIdType":"guid"}, 100)
print(symbol_list)
cap_list = {}

date = "CY2022"

cik_dict = {}
cik_list = []
for i in symbol_list:
    cik = "0" * (10-len(str(ciks[i.lower()]))) + str(ciks[i.lower()])
    cik_list.append(cik)
    cik_dict[i] = cik

for i in symbol_list:
    price = requests.get("https://query1.finance.yahoo.com/v6/finance/quoteSummary/"+ i +"?modules=price", cookies=cookies, headers=headers)
    # print(price.text)
    cap = json.loads(price.text)["quoteSummary"]["result"][0]["price"]["marketCap"]["raw"]
    cap_list[cik_dict[i]] = cap

def ranger(multiplicators, s):
    l_m = list(multiplicators.values())
    # print(list(filter(lambda x : x!= 0, list(filter(lambda x: x < 0, l_m)))))
    m_mean = np.mean(list(filter(lambda x: x < 0, l_m)))
    p_mean = np.mean(list(filter(lambda x: x > 0, l_m)))
    print("mean",m_mean, p_mean)
    if s=="+":
        val_list = list(map(lambda x: x / p_mean if x >= 0 else x / m_mean * (-1), l_m))
    else:
        val_list = list(map(lambda x: p_mean / x if x >= 0 else m_mean / x * (-1), l_m))
    val_list = [0 if str(x) == "inf" else x for x in val_list]
    multi_list = dict(zip(cik_list, val_list))

    return [multi_list, multiplicators]

def f(tags_input, s, formula, balanced, ratio):
    multi_list = {}
    multiplicators = {}
    data = []
    for i in tags_input: #добовляешь в data все тэги
        data.append(json.loads(requests.get("https://data.sec.gov/api/xbrl/frames/us-gaap/"+ i +"/USD/"+ date + ".json", cookies=cookies, headers=headers).text)["data"])
    print(data)
    # print("d0", data)
    for i in cik_list:
        tags_data = []
        for l in data: #перебираешь теги и добавляешь в список tags_data
            tags_data.append((list(filter(lambda x: x['cik'] == int(i), l)))) #находишь в списке из базы данных обьект с нужным сиком
        try:
            multiplicators[i] = eval(formula)
            print(multiplicators[i])
            # print(multiplicators)
        except IndexError:
            print(i, 'item is not in the list')
            multiplicators[i] = 0
    return ranger(multiplicators, s)

p_e = f(["NetIncomeLoss"], "-", "cap_list[i] / tags_data[0][0]['val']", 1, 1)
print("p_s")
p_s = f(["Revenues"], "-", "cap_list[i] / tags_data[0][0]['val']", 1, 1)



balanced = {"prices" : 8, "profitability" : 6, "health" : 5, "dividends" : 2, "growth" : 2}
ratio = {"prices" : 0.5, "profitability" : 1, "health" : 2, "dividends" : 0.5, "growth" : 1}


def sum_rang(l, name):
    super_list = {}
    print(symbol_list, cik_list)
    multi_list = {}
    multiplicators = {}
    print(l)
    for i in cik_list:
        sum_symbol = 0
        all_symbols = []
        for n in l:
            sum_symbol += n[0][i]
            all_symbols.append(n[1][i])
            all_symbols.append(n[0][i])
        all_symbols.append(sum_symbol)
        super_list[i] = all_symbols
        print(pd.DataFrame(data=super_list))
    return (pd.DataFrame(data=super_list, index=["p_e", "score", "p_s", "score", "itog"]).T).to_excel(name + '.xlsx')
print(sum_rang([p_e, p_s], "prices"))
