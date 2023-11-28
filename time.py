from parsers import Parser
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

def print_log(source, answer):
    print(f'{source.file:10} \t {source.type} \t {source.text_start} \t {source.text_end} \t {source.text:20} \t -> \t {answer} \t {source.answer} \t {"CORRECT" if answer == source.answer else "WRONG"}')

    

def main():
    file_name = 'total.txt'
    data = read_file(file_name)
    times = []
    for line in data:
        if len(line)>5:
            # print(line)
            time = Time(file=line[0], type=line[1], text_start=int(line[2]), text_end=int(line[3]), text=line[4], answer=line[5].strip())
            times.append(time)
    parser = Parser()

    output_file = 'output.csv'
    opt = open(output_file, 'w', encoding='UTF-8')

    correct = 0
    wrong = 0
    error = 0
    swaped_md=0
    for t in times:
        parse_type = -1
        ans = ''
        try:
            if t.type == 'TIME':
                # if 'at' in t.text: continue
                opt.write(f'{t.file},{t.type},{t.text_start},{t.text_end},{t.text},{t.answer},\n')
                print(f'{t.file} \t {t.type} \t {t.text_start} \t {t.text_end} \t {t.text:30} \t {t.answer:20}')
            else:
                continue          

            # print(f'{t.file} \t {t.type} \t {t.text_start} \t {t.text_end} \t {t.text:20} \t -> \t {ans} \t {t.answer} \t {"CORRECT" if ans == t.answer else "WRONG"}')

            if ans == t.answer: 
                correct += 1
            else:
                wrong += 1

                
        except Exception as e:
            print (e)
            print(f"{t.text} \t {t.answer} \t {parse_type}")
            print()
            error += 1

            print(f'{t.text} {t.answer}  ERROR')
        finally:
            pass

    print(f'Correct: {correct}, Wrong: {wrong}, Error: {error}, Swaped: {swaped_md}')
    print(f'Accuracy: {correct/(correct+wrong+error) * 100}%')

    opt.close()

if __name__ == '__main__':
    main()