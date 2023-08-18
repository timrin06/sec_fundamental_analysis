import fast_xbrl_parser as fxp
import pandas as pd
import time
import requests
from data.request_params import cookies, headers
import json

start = time.time()

inp= "https://www.sec.gov/Archives/edgar/data/875320/000087532022000038/vrtx-20220930_htm.xml" ## Edgar URL
#input = "gme-20211030_htm.xml" ## Local XML file


xbrl_dict = fxp.parse(
    inp, 
    output=['facts'],   ### You can adjust this to only return certain outputs. 
    email = "demo@fast-xbrl-parser.com"       ### Adjust this to reflect your email address. This is required by the SEC Edgar system when passing a URL.  
) 

facts_list = xbrl_dict['facts']
print(time.time()-start)
tags = [0]
for i in facts_list:
    if i != tags[-1]:
        tags.append(i['tag'])
print(tags)
l2 = json.loads(requests.get("https://data.sec.gov/api/xbrl/companyfacts/CIK0000875320.json", cookies=cookies, headers=headers).text)["facts"]["us-gaap"]
l2 = list(l2.keys())
s = set(l2)
temp3 = [x for x in tags if x not in s]
#print(temp3)
for i in temp3:
    pass
    #print(i)
#p = list(filter(lambda x: x['tag'] == 'CostOfGoodsAndServicesSold', facts_list))
#print(p)
#print(facts_list)
