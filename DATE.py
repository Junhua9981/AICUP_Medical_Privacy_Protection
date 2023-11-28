import dateutil.parser
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
    

def main():
    file_name = 'answer_first.txt'
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
        only_year = False
        parse_type = -1

        try:
            if t.type == 'DATE':
                if t.text.count('/') == 2:
                    parse_type = 1
                    d, m, y = map(int,t.text.split('/'))
                    if m > 12 : m, d = d, m
                    if y < 1000 : y = 2000 + y
                    time_str = datetime(y, m, d)

                elif t.text.count('.') == 2:
                    parse_type = 2
                    d, m, y = map(int,t.text.split('.'))
                    if m > 12 : m, d = d, m
                    if y < 1000 : y = 2000 + y
                    time_str = datetime(y, m, d)

                elif t.text.lower() == 'previous' or t.text.lower() == 'now' or t.text.lower() == 'today' or t.text.lower() == 'original':
                    parse_type = 3
                    time_str = datetime(y, m, d)

                elif len(t.text) == 4:
                    parse_type = 4
                    time_str = t.text
                    only_year = True

                else:
                    parse_type = 5
                    t.text = t.text.replace(',', ' ').replace('.', ' ')
                    time_str = dateutil.parser.parse(t.text)

            else: continue

            if only_year and t.text == t.answer: correct += 1
            elif time_str.strftime("%Y-%m-%d") == t.answer: correct += 1
            else:
                wrong += 1

                if time_str.strftime("%Y-%d-%m") == t.answer:
                    swaped_md += 1
                    # print(f'{t.file} {t.text_start} {t.text_end} \t {t.text:20} \t -> \t {time_str.strftime("%Y-%m-%d")} \t {t.answer} \t {"CORRECT" if time_str.strftime("%Y-%m-%d") == t.answer else "WRONG"}')
                else:
                    # print(f'{t.file} {t.text_start} {t.text_end} \t {t.text:20} \t -> \t {time_str.strftime("%Y-%m-%d")} \t {t.answer} \t {"CORRECT" if time_str.strftime("%Y-%m-%d") == t.answer else "WRONG"}')
                    pass
        except Exception as e:
            # print (e)
            # print(f"{t.text} \t {t.answer} \t {parse_type}")
            # print()
            error += 1

            # print(f'{t.text} {t.answer}  ERROR')
        finally:
            pass

    print(f'Correct: {correct}, Wrong: {wrong}, Error: {error}, Swaped: {swaped_md}')



if __name__ == '__main__':
    main()