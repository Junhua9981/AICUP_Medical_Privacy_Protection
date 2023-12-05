import re
from parsers.basic_parser import BasicParser

class DurationParser(BasicParser):
    def parse(self, text):
        ret = ''

        if len(re.findall(r'\d+', text)) == 2:
            num = map( lambda x: int(x), re.findall(r'\d+', text) ) 
            num = list(num)
            num = (num[0] + num[1])/2
            if 'd' in text:
                ret = f"P{num}D"
            
            elif 'y' in text:
                ret = f"P{num}Y"
            
            elif 'm' in text:
                ret = f"P{num}M"
            
            elif 'w' in text:
                ret = f"P{num}W"
        else:
            if 'd' in text:
                ret = f"P{DurationParser.extract_number(text)}D"
            
            elif 'y' in text:
                ret = f"P{DurationParser.extract_number(text)}Y"
            
            elif 'm' in text:
                ret = f"P{DurationParser.extract_number(text)}M"
            
            elif 'w' in text:
                ret = f"P{DurationParser.extract_number(text)}W"

        return ret


    @staticmethod
    def extract_number(text):
        text = text.lower()
        if 'eleven' in text: return 11
        elif 'twelve' in text: return 12
        elif 'thirteen' in text: return 13
        elif 'fourteen' in text: return 14
        elif 'fifteen' in text: return 15
        elif 'sixteen' in text: return 16
        elif 'seventeen' in text: return 17
        elif 'eighteen' in text: return 18
        elif 'nineteen' in text: return 19
        elif 'twenty' in text: return 20
        elif 'once' in text: return 1
        elif 'one' in text: return 1
        elif 'twice' in text: return 2
        elif 'two' in text: return 2
        elif 'thrice' in text: return 3
        elif 'three' in text: return 3
        elif 'four' in text: return 4
        elif 'five' in text: return 5
        elif 'six' in text: return 6
        elif 'seven' in text: return 7
        elif 'eight' in text: return 8
        elif 'nine' in text: return 9
        elif 'ten' in text: return 10
        
        else:
            numbers = re.findall(r'\d+', text)

            if len(numbers) == 0:
                raise ValueError(f'Cannot extract number from {text}')
            elif len(numbers) == 2:
                return numbers[1]-numbers[0]/2
            
            return re.findall(r'\d+', text)[0]