import requests
import json
from data.request_params import cookies, headers
from data.dannse import ciks
from get_list import get_list
import numpy as np
import pandas as pd
import fast_xbrl_parser

import time

start = time.time()

symbol_list = get_list(
    {"size": 25, "offset": 0, "sortField": "intradaymarketcap", "sortType": "DESC", "quoteType": "EQUITY",
     "topOperator": "AND", "query": {"operator": "AND", "operands": [
        {"operator": "or", "operands": [{"operator": "EQ", "operands": ["region", "us"]}]}, {"operator": "or",
                                                                                             "operands": [
                                                                                                 {"operator": "GT",
                                                                                                  "operands": [
                                                                                                      "intradaymarketcap",
                                                                                                      100000000000]},
                                                                                                 {"operator": "BTWN",
                                                                                                  "operands": [
                                                                                                      "intradaymarketcap",
                                                                                                      10000000000,
                                                                                                      100000000000]},
                                                                                                 {"operator": "BTWN",
                                                                                                  "operands": [
                                                                                                      "intradaymarketcap",
                                                                                                      2000000000,
                                                                                                      10000000000]}]},
        {"operator": "gt", "operands": ["intradayprice", 0]},
        {"operator": "or", "operands": [{"operator": "EQ", "operands": ["sector", "Healthcare"]}]},
        {"operator": "or", "operands": [{"operator": "EQ", "operands": ["industry", "Biotechnology"]}]},
        {"operator": "or", "operands": [{"operator": "EQ", "operands": ["exchange", "NAS"]},
                                        {"operator": "EQ", "operands": ["exchange", "NYQ"]},
                                        {"operator": "EQ", "operands": ["exchange", "YHD"]},
                                        {"operator": "EQ", "operands": ["exchange", "NGM"]},
                                        {"operator": "EQ", "operands": ["exchange", "NMS"]},
                                        {"operator": "EQ", "operands": ["exchange", "NCM"]},
                                        {"operator": "EQ", "operands": ["exchange", "BSE"]}]},
        {"operator": "or", "operands": [{"operator": "EQ", "operands": ["exchange", "NMS"]}]},
        {"operator": "gt", "operands": ["lastclosepricebookvalue.lasttwelvemonths", 0]},
        {"operator": "gt", "operands": ["lastclosepricetangiblebookvalue.lasttwelvemonths", 0]},
        {"operator": "gt", "operands": ["totalassets.lasttwelvemonths", 0]},
        {"operator": "gt", "operands": ["totalcurrentassets.lasttwelvemonths", 0]},
        {"operator": "gt", "operands": ["grossprofit.lasttwelvemonths", 0]},
        {"operator": "gt", "operands": ["lastclosemarketcaptotalrevenue.lasttwelvemonths", 0]}]}, "userId": "",
     "userIdType": "guid"}, 100)
print(symbol_list)
cap_list = {}

date = "CY2022"
fp = "FY"
fy = 2022

cik_dict = {}
cik_list = []
for i in symbol_list:
    cik = "0" * (10 - len(str(ciks[i.lower()]))) + str(ciks[i.lower()])
    cik_list.append(cik)
    cik_dict[i] = cik

for i in symbol_list:
    price = requests.get("https://query1.finance.yahoo.com/v6/finance/quoteSummary/" + i + "?modules=price",
                         cookies=cookies, headers=headers)
    # print(price.text)
    cap = json.loads(price.text)["quoteSummary"]["result"][0]["price"]["marketCap"]["raw"]
    cap_list[cik_dict[i]] = cap


def ranger(multiplicators, s):
    l_m = list(multiplicators.values())
    # print(list(filter(lambda x : x!= 0, list(filter(lambda x: x < 0, l_m)))))
    m_mean = np.mean(list(filter(lambda x: x < 0, l_m)))
    p_mean = np.mean(list(filter(lambda x: x > 0, l_m)))
    print("mean", m_mean, p_mean)
    if s == "+":
        val_list = list(map(lambda x: x / p_mean * 2 if x >= 0 else m_mean / x, l_m))
    else:
        val_list = list(map(lambda x: p_mean / x * 2 if x >= 0 else x / m_mean, l_m))
    val_list = [0 if str(x) == "inf" else x for x in val_list]
    multi_list = dict(zip(cik_list, val_list))

    return [multi_list, multiplicators]

def filter_frame():
    pass

def f(tags_input, s, formula, balanced, ratio):
    multiplicators = {}
    data = []
    for i in cik_list:
        data = json.loads(requests.get("https://data.sec.gov/api/xbrl/companyfacts/CIK" + i + ".json", cookies=cookies, headers=headers).text)["facts"]
        for i1 in tags_input:
            try:
                e = []
                for i2 in i1:
                    tag = data["us-gaap"][i2]
                    l = list(filter(lambda x: x["fy"] == fy, tag["units"]["USD"]))
                    l = (list(filter(lambda x: x["fp"] == fp, l)))
                    e.append(list(filter(lambda x: x["frame"] == date, l))[0])
                multiplicators[i] = eval(formula)
                print(i2)
                break
            except KeyError:
                print(i, 'item is not in the list, keyerror')
                multiplicators[i] = 0
            except IndexError:
                print(i, 'item is not in the list, indexerror')
                multiplicators[i] = 0
    return ranger(multiplicators, s)

print("p_gp")
p_gp = f([
    ["RevenueFromContractWithCustomerExcludingAssessedTax", "CostOfGoodsAndServicesSold"],
    ["RevenueFromContractWithCustomerIncludingAssessedTax", "CostOfGoodsAndServicesSold"],
    ["Revenues", "CostOfGoodsAndServicesSold"],
    ["RevenueFromContractWithCustomerExcludingAssessedTax", "CostOfRevenue"],
    ["RevenueFromContractWithCustomerIncludingAssessedTax", "CostOfRevenue"],
    ["Revenues", "CostOfRevenue"],
    ["RevenueFromContractWithCustomerExcludingAssessedTax","CostOfGoodsAndServicesSoldDepreciation"],
    ["RevenueFromContractWithCustomerIncludingAssessedTax","CostOfGoodsAndServicesSoldDepreciation"],
    ["Revenues","CostOfGoodsAndServicesSoldDepreciation"]
],

    "-", "cap_list[i] / (e[0]['val']-e[1]['val'])", 1, 1)
print("p_e")
p_e = f([["NetIncomeLoss"], ["NetIncomeLossAvailableToCommonStockholdersBasic"]], "-", "cap_list[i] / e[0]['val']", 1, 1)
print(time.time() - start)
print("p_s")
p_s = f([["RevenueFromContractWithCustomerExcludingAssessedTax"], ["Revenues"],
         ["RevenueFromContractWithCustomerIncludingAssessedTax"]], "-", "cap_list[i] / e[0]['val']", 1, 1)
print(time.time() - start)
print("p_bv")
p_bv = f([["Assets", "Liabilities"]], "-", "cap_list[i] / (e[0]['val']-e[1]['val'])", 1, 1)
print(time.time() - start)


balanced = {"prices": 8, "profitability": 6, "health": 5, "dividends": 2, "growth": 2}
ratio = {"prices": 0.5, "profitability": 1, "health": 2, "dividends": 0.5, "growth": 1}


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
        super_list[i + "  " + list(cik_dict.keys())[list(cik_dict.values()).index(i)]] = all_symbols
        print(pd.DataFrame(data=super_list))
    return (pd.DataFrame(data=super_list, index=["p_e", "score", "p_s", "score", "p_gp", "score", "itog"]).T).to_excel(
        name + '.xlsx')


print(sum_rang([p_e, p_s, p_gp], "prices"))

end = time.time() - start
print(end)