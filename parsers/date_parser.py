from parsers.basic_parser import BasicParser
from datetime import datetime
import dateutil.parser
import re

class DateParser(BasicParser):
    def __init__(self):
        self.y = 1
        self.m = 1
        self.d = 1

    def parse(self, text):

        if len( re.findall(r'\/\d+\/\d+', text) ) == 1 and re.findall(r'\/\d+\/\d+', text)[0] == text:
            date = re.findall(r'\/\d+\/\d+', text)[0]
            date = date.split('/')
            return f"{date[2] if len(date[2]) == 4 else '20'+date[2]}-{int(date[1]):02d}"
        elif len( re.findall(r'\d+\/\d+\/', text) ) == 1 and re.findall(r'\d+\/\d+\/', text)[0] == text:
            date = re.findall(r'\d+\/\d+\/', text)[0]
            date = date.split('/')
            return f"{date[0] if len(date[0]) == 4 else '20'+date[0]}-{int(date[1]):02d}"
        
        if len( re.findall(r'\.\d+\.\d+', text) ) == 1 and re.findall(r'\.\d+\.\d+', text)[0] == text:
            date = re.findall(r'\.\d+\.\d+', text)[0]
            date = date.split('.')
            return f"{date[2] if len(date[2]) == 4 else '20'+date[2]}-{int(date[1]):02d}"
        elif len( re.findall(r'\d+\.\d+\.', text) ) == 1 and re.findall(r'\d+\.\d+\.', text)[0] == text:
            date = re.findall(r'\d+\.\d+\.', text)[0]
            date = date.split('.')
            return f"{date[0] if len(date[0]) == 4 else '20'+date[0]}-{int(date[1]):02d}"

        if len( re.findall(r'\d+\/\d+', text) ) == 1 and re.findall(r'\d+\/\d+', text)[0] == text:
            date = re.findall(r'\d+', text)
            return f"{date[1] if len(date[1]) == 4 else '20'+date[1]}-{int(date[0]):02d}"

        only_year = False
        time_str = text
        if text.count('/') == 2:
            d, m, y = map(int, re.findall(r'\d+', text))
            if m > 12 : m, d = d, m
            if y < 1000 : y = 2000 + y
            time_str = datetime(y, m, d)
            self.y=y
            self.m=m
            self.d=d

        elif text.count('.') == 2:
            d, m, y = map(int, re.findall(r'\d+', text))
            if m > 12 : m, d = d, m
            if y < 1000 : y = 2000 + y
            time_str = datetime(y, m, d)
            self.y=y
            self.m=m
            self.d=d

        elif text.lower() == 'previous' or text.lower() == 'now' or text.lower() == 'today' or text.lower() == 'original':
            time_str = datetime(self.y, self.m, self.d)

        elif len(text) == 4 and text.isdigit():
            time_str = text
            only_year = True
            return text

        else:
            text = text.replace(',', ' ').replace('.', ' ')
            time_str = dateutil.parser.parse(text)
            self.y = time_str.year
            self.m = time_str.month
            self.d = time_str.day


        if only_year:
            return time_str
        elif time_str.year < 1000:
            time_str = datetime(time_str.year + 2000, time_str.month, time_str.day)
            return datetime.strftime(time_str, "%Y-%m-%d")
        
        return datetime.strftime(time_str, "%Y-%m-%d") if not only_year else time_str