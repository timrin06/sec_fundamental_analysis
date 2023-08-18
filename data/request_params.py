cookies = {
    'A1': 'd=AQABBLVgQGMCEJV5A8mGAq5zpwFnODIwbtIFEgEBAQGyQWNKYwAAAAAA_eMAAA&S=AQAAAiTNMtyQXTmCHSGpeB8Ek84',
    'A3': 'd=AQABBLVgQGMCEJV5A8mGAq5zpwFnODIwbtIFEgEBAQGyQWNKYwAAAAAA_eMAAA&S=AQAAAiTNMtyQXTmCHSGpeB8Ek84',
    'A1S': 'd=AQABBLVgQGMCEJV5A8mGAq5zpwFnODIwbtIFEgEBAQGyQWNKYwAAAAAA_eMAAA&S=AQAAAiTNMtyQXTmCHSGpeB8Ek84&j=WORLD',
    'cmp': 't=1665163447&j=0&u=1---',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0',
    'Accept': '*/*',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://finance.yahoo.com/screener/unsaved/2ba205e7-cc2f-4eb6-b35d-38dad8b136bb?offset=25&count=25',
    # Already added when you pass json=
    # 'Content-Type': 'application/json',
    'Origin': 'https://finance.yahoo.com',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'A1=d=AQABBLVgQGMCEJV5A8mGAq5zpwFnODIwbtIFEgEBAQGyQWNKYwAAAAAA_eMAAA&S=AQAAAiTNMtyQXTmCHSGpeB8Ek84; A3=d=AQABBLVgQGMCEJV5A8mGAq5zpwFnODIwbtIFEgEBAQGyQWNKYwAAAAAA_eMAAA&S=AQAAAiTNMtyQXTmCHSGpeB8Ek84; A1S=d=AQABBLVgQGMCEJV5A8mGAq5zpwFnODIwbtIFEgEBAQGyQWNKYwAAAAAA_eMAAA&S=AQAAAiTNMtyQXTmCHSGpeB8Ek84&j=WORLD; cmp=t=1665163447&j=0&u=1---',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    # Requests doesn't support trailers
    # 'TE': 'trailers',
}

params = {
    'crumb': 'G42sbf2QpHN',
    'lang': 'en-US',
    'region': 'US',
    'formatted': 'true',
    'corsDomain': 'finance.yahoo.com',
}
