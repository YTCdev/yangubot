import dateutil.parser
from pandas.tseries.offsets import BDay
from config import Config

class Order:
    def __init__(self, json, notes):
        self.json = json
        self.notes = notes

    def parse_date(self, date_str):
        return dateutil.parser.parse(date_str)

    def calc_bdays(self, date, days):
        return date + BDay(days)
