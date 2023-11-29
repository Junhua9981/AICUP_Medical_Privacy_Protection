from parsers.date_parser  import DateParser
from parsers.set_parser import SetParser
from parsers.duration_parser import DurationParser
from parsers.time_parser import TimeParser

class Parser:
    def __init__(self):
        self.parsers = {
            'DATE': DateParser(),
            'SET': SetParser(),
            'DURATION': DurationParser(),
            'TIME': TimeParser()
        }

    def parse(self, text, type):
        return self.parsers[type].parse(text)