import re
from parsers.basic_parser import BasicParser

class SetParser(BasicParser):
    def parse(self, text):
        return f'R{SetParser.extract_times(text)}' 

    @staticmethod
    def extract_times(text):
        text = text.lower()
        if   'once' in text: return 1
        elif 'twice' in text: return 2
        elif 'thrice' in text: return 3
        elif 'three' in text: return 3
        elif 'four' in text: return 4
        elif 'five' in text: return 5
        elif 'six' in text: return 6
        elif 'seven' in text: return 7
        elif 'eight' in text: return 8
        elif 'nine' in text: return 9
        elif 'ten' in text: return 10
        elif 'eleven' in text: return 11
        elif 'twelve' in text: return 12
        elif 'thirteen' in text: return 13
        elif 'fourteen' in text: return 14
        elif 'fifteen' in text: return 15
        elif 'sixteen' in text: return 16
        elif 'seventeen' in text: return 17
        elif 'eighteen' in text: return 18
        elif 'nineteen' in text: return 19
        elif 'twenty' in text: return 20
        else:
            numbers = re.findall(r'\d+', text)
            if len(numbers) == 0:
                raise ValueError(f'Cannot extract number from {text}')
            elif len(numbers) == 2:
                return numbers[1]-numbers[0]/2
            
            return re.findall(r'\d+', text)[0]