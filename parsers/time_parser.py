from parsers.basic_parser import BasicParser
from datetime import datetime
import dateutil.parser
import re   

class TimeParser(BasicParser):
    def parse(self, text):
        # print(text)
        text = text.lower()
        has_sec = False
        if 'at' in text or 'on' in text or '@' in text:
            if 'at' in text:
                text = text.replace('fcs1', '')
                text = text.replace('insrsid8013677', '')
                date, time = text.split('at')
            elif 'on' in text:
                time, date = text.split('on')
            elif '@' in text:
                time, date = text.split('@')
        
            if 'am' in date or 'pm' in date:
                date, time = time, date

            try:
                date = TimeParser.extract_date(date)
            except:
                date = dateutil.parser.parse(date)

            if len(re.findall(r'\d+', time)) == 3 or len(re.findall(r'\d+', time)) == 6:
                has_sec = True
            
            time, has_sec = TimeParser.extrac_time(time)
        
        elif len(re.findall(r'\d+', text)) == 6:

            has_sec = True
            date = re.findall(r'\d+', text)
            if len(re.findall(r'\d+', text)[0])==4:
                date = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))
                time = date
            
            elif len(re.findall(r'\d+', text)[2])==4:
                date = datetime(int(date[2]), int(date[1]), int(date[0]), int(date[3]), int(date[4]), int(date[5]))
                time = date
        
        elif len(re.findall(r'\d+', text)) == 5:
            date = re.findall(r'\d+', text)
            # print(date)
            if len(re.findall(r'\d+', text)[0])==4:
                date = datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]))
                time = date
            
            elif len(re.findall(r'\d+', text)[2])==4:
                date = datetime(int(date[2]), int(date[1]), int(date[0]), int(date[3]), int(date[4]))
                time = date

            else:
                if 'pm' in text and text.index('pm') < len(text) / 2 +3:
                    date = datetime(int(date[4]), int(date[3]), int(date[2]), int(date[0])+(12 if int(date[0])<12 else 0), int(date[1].replace('pm', '')))
                    time = date
                elif 'am' in text and text.index('am') < len(text) / 2 +3:
                    date = datetime(int(date[4]), int(date[3]), int(date[2]), int(date[0]), int(date[1].replace('am', '')))
                    time = date
                elif 'pm' in text :
                    date = datetime(int(date[2]), int(date[1]), int(date[0])+(12 if int(date[0])<12 else 0), int(date[3]), int(date[4]))
                    time = date
                elif 'am' in text :
                    date = datetime(int(date[2]), int(date[1]), int(date[0]), int(date[3]), int(date[4]))
                    time = date
                else:
                    date = datetime(int(date[4]), int(date[3]), int(date[2]), int(date[0]), int(date[1]))
                    time = date
        else:
            return None, None, None
        try:
            if has_sec:
                return datetime.strftime(datetime(date.year, date.month, date.day, time.hour, time.minute, time.second), "%Y-%m-%dT%H:%M:%S")
            return datetime.strftime(datetime(date.year, date.month, date.day, time.hour, time.minute, time.second), "%Y-%m-%dT%H:%M")
        except:
            return None, None, None

    @staticmethod
    def extract_date(txt):
        txt = txt.lower()
        txt = txt.replace(',', '-').replace('.', '-').replace('/', '-')
        if len( re.findall(r'\d+', txt) ) == 3:
            d, m, y = map(int, re.findall(r'\d+', txt))
            if m > 12 and d >31: 
                m = m%12
                d = d%31

            if m > 12 and d <= 12 : m, d = d, m
            if y < 1000 : y = 2000 + y
            return datetime(y, m, d)
        elif 'of' in txt:
            month_dict = {
                'january': 1, 'february': 2, 'march': 3, 'april': 4,
                'may': 5, 'june': 6, 'july': 7, 'august': 8,
                'september': 9, 'october': 10, 'november': 11, 'december': 12
            }
            for month in month_dict.keys():
                if month in txt:
                    m = month_dict[month]
                    break
            d = int(re.findall(r'\d+', txt)[0])
            y = int(re.findall(r'\d+', txt)[1])
            return datetime(y, m, d)
            

    @staticmethod
    def extrac_time(txt):
        txt = txt.lower()
        has_sec = False
        eps = 0

        if 'am' in txt:
            txt = txt.replace('am', '')
        elif 'pm' in txt :
            txt = txt.replace('pm', '')
            eps = 12

        txt = txt.replace('.', '').replace(',', '').replace(':', '')
        time = re.findall(r'\d+', txt)[0]
        if len(time) == 5:   # hmmss
            time = '0' + time
            time = datetime(1,1,1, int(time[:2]), int(time[2:4]), int(time[4:6]))
            has_sec = True
        elif len(time) == 6: # hhmmss
            time = datetime(1,1,1, int(time[:2]), int(time[2:4]), int(time[4:6]))
            has_sec = True
        elif len(time) == 4: # hhmm
            time = datetime(1,1,1, int(time[:2]), int(time[2:4]))
        elif len(time) == 3:
            time = datetime(1,1,1, int(time[:1]), int(time[1:3]))
        elif len(time) == 2:
            time = datetime(1,1,1, int(time[:2]), 0)
        elif len(time) == 1:
            time = datetime(1,1,1, int(time[:1]), 0)
        else:
            time = datetime(1,1,1, int(time[:2]), int(time[2:4]))
        
        if eps != 0 and time.hour == 12:
            eps = 0
        try:
            time = time.replace(hour=time.hour+eps)
        except:
            time = time.replace(hour=time.hour)
        return time, has_sec

        