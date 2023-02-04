import logging
import json 
import urllib.parse

import azure.functions as func

from .methods import get_ticker_price_changed

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    logging.info(f"TAL::: {req.url}")
    url_parts = urllib.parse.urlparse(current_url)
    logging.info (f"TAL::: {url_parts.hostname}")
                 
    ticker = req.params.get('ticker')
    start_date = req.params.get('start_date')
    end_date = req.params.get('end_date')

    if not ticker:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            ticker = req_body.get('ticker')
            start_date=req_body.get('start_date')
            end_date=req_body.get('end_date')


    if ticker:
        logging.info (f"get_ticker_price_changed::init:main: Ticker:{ticker}, Start_date:{start_date}, End_date:{end_date}")
        data = get_ticker_price_changed(ticker=ticker, start_date=start_date, end_date=end_date)
        return func.HttpResponse(json.dumps(data), status_code=200)
    else:
        err = {"error":"Ticker is not provided"}
        logging.info (err)
        return func.HttpResponse(json.dumps(err), status_code=400)
