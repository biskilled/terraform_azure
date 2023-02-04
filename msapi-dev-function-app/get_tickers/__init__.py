import logging

import azure.functions as func

from get_tickers.methods import get_tickers_marketstack

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

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
        logging.info ("get_tickers: Ticker:{ticker}, Start_date:{start_date}, End_date:{end_date}")
        api = get_tickers_marketstack()
        res = api.get_tickers_OHLCV(ticker=ticker, start_date=start_date, end_date=end_date)
        return func.HttpResponse(res, status_code=200)
    
    else:
        err = {"error":"Ticker is not provided"}
        logging.info (err)
        return func.HttpResponse(err, status_code=400)
    
