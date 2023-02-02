"""
provide a stock ticker and be returned a JSON response of end-of-day pricing
API https://marketstack.com
user: myzevel@yahoo.com pass: yoyo4Market!
API Key = 07a347c645898d0bda9f41e7ed0f9e5d
"""


import requests
import datetime

API_KEY = '07a347c645898d0bda9f41e7ed0f9e5d'

class get_ticks_marketstack():
    def __init__ (self, api_key, date_format='%Y-%m-%d'):
        self.api_key = api_key
        self.date_format = date_format
        self.api_url = "http://api.marketstack.com/v1"
        self.batch_size = 100
        self.default_last_days = 100
        self.all_data = {}

    def _is_valid_date_format(self, date_string):
        try:
            datetime.datetime.strptime(date_string, self.date_format)
            return True
        except ValueError:
            return False

    def _get_eod_pricing(self, symbol, start_date, end_date):
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
            ret = {item['date']:item['close'] for item in data['data']}
            return ret
        else:
            print (f"ERROR FETCHING DATA ! ")
        return {}

    def get_stock_price(self, ticker, start_date=None, end_date=None):
        if ticker not in self.all_data:
            self.all_data[ticker] = {}
        current_date = datetime.datetime.now()
        if not end_date:
            end_date = current_date
            # end_date = current_date.strftime(self.date_format)
        else:
            if not self._is_valid_date_format(end_date):
                print (f"END DAY NOT VALID, MUST USE {self.date_format} FORMAT")
                return
            end_date = datetime.datetime.strptime(end_date, self.date_format)

        if not start_date:
            start_date = (current_date - datetime.timedelta(days=self.default_last_days))
        else:
            if not self._is_valid_date_format(start_date):
                print (f"START DAY NOT VALID, MUST USE '%Y-%m-%d' FORMAT")
                return
            start_date = datetime.datetime.strptime(start_date, self.date_format)

        current_start_date = start_date

        while current_start_date < end_date:
            current_end_date = current_start_date + datetime.timedelta(days=self.batch_size - 1)
            if current_end_date > end_date:
                current_end_date = end_date

            eod_pricing = self._get_eod_pricing(ticker, current_start_date, current_end_date)
            self.all_data[ticker].update (eod_pricing)

            current_start_date = current_end_date + datetime.timedelta(days=1)
        return self.all_data[ticker]

""" TESTS """
api = get_ticks_marketstack(api_key=API_KEY)
res = api.get_stock_price(ticker="AAPL", start_date="2022-09-01", end_date=None)
# return dictionay with date and closing price

for i,item in enumerate (res):
    print (i,item, res[item])