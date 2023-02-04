import requests
import json
import logging  
import socket

def _invoke_api (api_name, ticker, start_date, end_date=None):
    
    function_url = f"https://{req.host.split('.')[0]}/api/{api_name}?ticker={ticker}&start_date={start_date}"

    if end_date:
        function_url +=f"&end_date={end_date}"

    logging.info (f"get_ticker_price_changed: using Url {function_url}")
    response = requests.get(function_url)

    if response.status_code != 200:
        return {'error_code':response.status_code, 'error':response.content}

    return response.json()

def price_changed (ticker, result):
    if 'data' in result:
        ret = {ticker:None}
        latest_price = result['data'][-1]['close']
        oldest_price = result['data'][0]['close']
        ret[ticker] = latest_price - oldest_price
        return  ret 
    else:
        return {'error':f"{ticker}: Cannot find any data in {result}"}    

def get_ticker_price_changed(ticker, start_date, end_date=None):
    logging.info (f"get_ticker_price_changed in: Ticker:{ticker}, Start_date:{start_date}, End_date:{end_date}")
    if not ticker:
        err = f"Must provide ticker {ticker}"
        logging.info (err)
        return {"error":err}

    result = _invoke_api (api_name='get_tickers', ticker=ticker, start_date=start_date, end_date=end_date)
    return price_changed (ticker=ticker, result=result)
