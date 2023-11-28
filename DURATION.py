import dateutil.parser
import re
from datetime import datetime
from dataclasses import dataclass

@dataclass
class Time:
    file : str
    type : str
    text_start : int
    text_end : int
    text : str
    answer : str



def read_file(file_name):
    with open(file_name, 'r', encoding="UTF-8") as f:
        lines = f.readlines()
        result = map(lambda x: x.split('\t'), lines)
        return list(result)
    
def save_data(file_name, data):
    with open(file_name, 'w') as f:
        for line in data:
            f.write('\t'.join(line))
            f.write('\n')
    
def extract_number(text):
    if   'one' in text: return 1
    elif 'two' in text: return 2
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
        return re.findall(r'\d+', text)[0]


def main():
    file_name = 'answer.txt'
    data = read_file(file_name)
    times = []
    for line in data:
        if len(line)>5:
            # print(line)
            time = Time(file=line[0], type=line[1], text_start=int(line[2]), text_end=int(line[3]), text=line[4], answer=line[5].strip())
            times.append(time)


    correct = 0
    wrong = 0
    error = 0
    swaped_md=0
    for t in times:
        parse_type = -1

        try:
            if t.type == 'DURATION':

                if 'd' in t.text:
                    ans = f"P{extract_number(t.text)}D"
                    
                elif 'y' in t.text:
                    ans = f"P{extract_number(t.text)}Y"
                
                elif 'm' in t.text:
                    ans = f"P{extract_number(t.text)}M"
                
                elif 'w' in t.text:
                    ans = f"P{extract_number(t.text)}W"

                else:
                    error += 1

            else: continue

            print(f'{t.file} {t.text_start} {t.text_end} \t {t.text:20} \t -> \t {ans} \t {t.answer} \t {"CORRECT" if ans == t.answer else "WRONG"}')

            if ans == t.answer: 
                correct += 1
            else:
                wrong += 1

                
        except Exception as e:
            # print (e)
            # print(f"{t.text} \t {t.answer} \t {parse_type}")
            # print()
            error += 1

            print(f'{t.text} {t.answer}  ERROR')
        finally:
            pass

    print(f'Correct: {correct}, Wrong: {wrong}, Error: {error}, Swaped: {swaped_md}')
    print(f'Accuracy: {correct/(correct+wrong+error)}')



if __name__ == '__main__':
    main()