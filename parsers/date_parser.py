from parsers.basic_parser import BasicParser
from datetime import datetime
import dateutil.parser

class DateParser(BasicParser):
    def __init__(self):
        self.y = 1
        self.m = 1
        self.d = 1

    def parse(self, text):
        only_year = False
        time_str = text
        if text.count('/') == 2:
            d, m, y = map(int, text.split('/'))
            if m > 12 : m, d = d, m
            if y < 1000 : y = 2000 + y
            time_str = datetime(y, m, d)
            self.y=y
            self.m=m
            self.d=d

        elif text.count('.') == 2:
            d, m, y = map(int, text.split('.'))
            if m > 12 : m, d = d, m
            if y < 1000 : y = 2000 + y
            time_str = datetime(y, m, d)
            self.y=y
            self.m=m
            self.d=d

        elif text.lower() == 'previous' or text.lower() == 'now' or text.lower() == 'today' or text.lower() == 'original':
            time_str = datetime(self.y, self.m, self.d)

        elif len(text) == 4:
            time_str = text
            only_year = True

        else:
            text = text.replace(',', ' ').replace('.', ' ')
            time_str = dateutil.parser.parse(text)
            self.y = time_str.year
            self.m = time_str.month
            self.d = time_str.day



        return datetime.strftime(time_str, "%Y-%m-%d") if not only_year else time_str