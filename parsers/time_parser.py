from parsers.basic_parser import BasicParser
from datetime import datetime
import dateutil.parser
import re   

class TimeParser(BasicParser):
    def parse(self, text):
        text = text.lower()
        has_sec = False

        if 'at' in text:
            date, time = text.split('at')
            if len(re.findall(r'\d+', time)) == 2:
                date = date.replace('th', '').replace('st', '').replace('nd', '').replace('rd', '').replace('of', '')
                date = date.split(' ')
                if len(date) == 3:
                    for d in date: d = d.strip()
                    d[1] = d[1][:3]
                    date = '-'.join(d)
                else:
                    date = '-'.join(date)
            date = date.replace(',', '-').replace('.', '-').replace('/', '-')
            try:
                date = dateutil.parser.parse(date)
            except:
                raise ValueError(f'Cannot parse date {date}')

            if len(re.findall(r'\d+', time)) == 3:
                has_sec = True
            
            time = TimeParser.extrac_time(time)

        elif 'on' in text:
            time, date = text.split('on')
            
            if 'am' in date or 'pm' in date:
                date, time = time, date
            
            time = TimeParser.extrac_time(time)

            date.replace(',', '-').replace('.', '-')
            if date.count('-') == 2:
                d, m, y = map(int, date.split('-'))
                if m > 12 : m, d = d, m
                if y < 1000 : y = 2000 + y
                date = datetime(y, m, d)
            elif 'of' in date:  ##the 25th of September 2013
                date = date.replace('of', '').replace('th', '').replace('st', '').replace('nd', '').replace('rd', '')
                date = dateutil.parser.parse(date)
            else:
                date = dateutil.parser.parse(date)
            
            
        elif '@' in text:
            time, date = text.split('@')
            if len(re.findall(r'\d+', time)) == 3: ## time 可能會有秒 所以這邊錯
                time, date = date, time

            time = TimeParser.extrac_time(time)

            date.replace(',', '-').replace('.', '-')
            date = dateutil.parser.parse(date)
        
        elif len(re.findall(r'\d+', text)) == 6:
            has_sec = True
            date = re.findall(r'\d+', text)
            if len(re.findall(r'\d+', text)[0])==4:
                date = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))
                time = datetime(1,1,1, date.hour, date.minute, date.second)

            else:
                date = datetime(int(date[3]), int(date[4]), int(date[5]), int(date[0]), int(date[1]), int(date[2]))
                time = datetime(int(date[3]), int(date[4]), int(date[5]), int(date[0]), int(date[1]), int(date[2]))

        
        else:
            date = dateutil.parser.parse(text)
            time = datetime(date.year, date.month, date.day, 0, 0, 0)

        if has_sec:
            return datetime.strftime(datetime(date.year, date.month, date.day, time.hour, time.minute, time.second), "%Y-%m-%dT%H:%M:%S")
        return datetime.strftime(datetime(date.year, date.month, date.day, time.hour, time.minute, time.second), "%Y-%m-%dT%H:%M")


    @staticmethod
    def extrac_time(txt):
        txt = txt.lower()

        eps = 0

        if 'am' in txt:
            txt = txt.replace('am', '')
        elif 'pm' in txt :
            txt = txt.replace('pm', '')
            eps = 12

        txt = txt.replace('.', '').replace(',', '').replace(':', '')
        time = re.findall(r'\d+', txt)[0]
        if len(time) == 5: ##hmmss
            time = '0' + time
            time = datetime(1,1,1, int(time[:2]), int(time[2:4]), int(time[4:6]))
        elif len(time) == 6:
            time = datetime(1,1,1, int(time[:2]), int(time[2:4]), int(time[4:6]))
        elif len(time) == 4:
            time = datetime(1,1,1, int(time[:2]), int(time[2:4]))
        elif len(time) == 3:
            time = datetime(1,1,1, int(time[:1]), int(time[1:3]))
        else:
            time = datetime(1,1,1, int(time[:2]), int(time[2:4]))
        
        if eps != 0 and time.hour == 12:
            eps = 0
        time = time.replace(hour=time.hour+eps)
        return time

        