import requests
import json
import logging  
import urllib.parse

def _get_host (url):
    url_parts = urllib.parse.urlparse(url)
    return url_parts.hostname

def _invoke_api (url, api_name, ticker, start_date, end_date=None):
    url_host = _get_host(url)
    logging.info (f"_invoke_api: Using URL {url_host}")
    function_url = f"https://{url_host}/api/{api_name}?ticker={ticker}"
    
    if start_date:
        function_url +=f"&start_date={start_date}"

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

def get_ticker_price_changed(current_url, ticker, start_date, end_date=None):
    logging.info (f"get_ticker_price_changed in: Ticker:{ticker}, Start_date:{start_date}, End_date:{end_date}")
    if not ticker:
        err = f"Must provide ticker {ticker}"
        logging.info (err)
        return {"error":err}

    result = _invoke_api (url=current_url, api_name='get_tickers', ticker=ticker, start_date=start_date, end_date=end_date)
    return price_changed (ticker=ticker, result=result)
