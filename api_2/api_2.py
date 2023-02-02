import datetime

from api_1 import get_ticks_marketstack

class extend_get_ticks_marketstack (get_ticks_marketstack):

    def get_price_change(self, symbol, num_days):
        today = datetime.datetime.now()
        end_date = today - datetime.timedelta(days=1)
        start_date = end_date - datetime.timedelta(days=num_days)

        eod_pricing = self.get_stock_price(symbol, start_date, end_date)
        latest_price = eod_pricing['data'][-1]['close']
        oldest_price = eod_pricing['data'][0]['close']

        change = latest_price - oldest_price
        return change


symbol = 'AAPL'
num_days = 30
change = get_price_change(symbol, num_days)
print(f'Change in price for {symbol} over the last {num_days} days: {change}')
