"""
provide a stock ticker and be returned a JSON response of end-of-day pricing
API https://marketstack.com
user: myzevel@yahoo.com pass: yoyo4Market!
API Key = 07a347c645898d0bda9f41e7ed0f9e5d
"""


import requests
import datetime
import os
import logging

#todo: MS_API_KEY API_KEY IN AZURE SECRET 
API_KEY = os.environ.get('MS_API_KEY') #'07a347c645898d0bda9f41e7ed0f9e5d'

logging.info (os.environ)
class get_tickers_marketstack():
    def __init__ (self, api_key=API_KEY, date_format='%Y-%m-%d'):
        self.api_key = api_key
        self.date_format = date_format
        self.api_url = "http://api.marketstack.com/v1"
        self.batch_size = 100
        self.default_last_days = 100

    def _is_valid_date_format(self, date_string):
        try:
            datetime.datetime.strptime(date_string, self.date_format)
            return True
        except ValueError:
            return False

    def _get_eod (self, symbol, start_date, end_date):
        url = f'{self.api_url}/eod'
        params = {
            'access_key': API_KEY,
            'symbols': symbol,
            'date_from': start_date.strftime(self.date_format),
            'date_to': end_date.strftime(self.date_format)
        }

        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            return data['data']
        else:
            print (f"ERROR FETCHING DATA ! ")
        return {'data':[]}

    def get_tickers_OHLCV (self, ticker, start_date=None, end_date=None):
        ret = {'data':[]}

        if not ticker:
            err = f"Must provide ticker - {ticker}"
            logging.info (err)
            return {"error":err}

        current_date = datetime.datetime.now()
        if not end_date:
            end_date = current_date
            # end_date = current_date.strftime(self.date_format)
        else:
            if not self._is_valid_date_format(end_date):
                err = f"END DAY NOT VALID, MUST USE {self.date_format} FORMAT"
                logging.info (err)
                return {"error":err}
            end_date = datetime.datetime.strptime(end_date, self.date_format)

        if not start_date:
            start_date = (current_date - datetime.timedelta(days=self.default_last_days))
        else:
            if not self._is_valid_date_format(start_date):
                err = f"START DAY NOT VALID, MUST USE '%Y-%m-%d' FORMAT"
                logging.info (err)
                return {"error":err}
            start_date = datetime.datetime.strptime(start_date, self.date_format)

        current_start_date = start_date

        logging.info (f"get_tickers_OHLCV: TICKER {ticker}, Start_date: {start_date.strftime(self.date_format)}, End_date:{end_date.strftime(self.date_format)}")
        while current_start_date < end_date:
            current_end_date = current_start_date + datetime.timedelta(days=self.batch_size - 1)
            if current_end_date > end_date:
                current_end_date = end_date

            eod_pricing = self._get_eod(ticker, current_start_date, current_end_date)
            ret['data'].extend(eod_pricing)

            current_start_date = current_end_date + datetime.timedelta(days=1)
        return ret 
    
