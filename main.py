from parsers import Parser
from dataclasses import dataclass
import sys
import traceback
import argparse

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

def print_log(source, answer, is_error=False):
    if is_error:
        print(f'{source.file:10} \t {source.type} \t {source.text_start} \t {source.text_end} \t {source.text:20} \t -> \t {" "*15} \t {source.answer:10} \t {"ERROR"}')
    else:
        print(f'{source.file:10} \t {source.type} \t {source.text_start} \t {source.text_end} \t {source.text:20} \t -> \t {str(answer):15} \t {source.answer:10} \t {"CORRECT" if answer == source.answer else "WRONG"}')


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--file', type=str, default='answer.txt')
    args = parser.parse_args()
    file_name = args.file

    data = read_file(file_name)
    times = []
    for line in data:
        if len(line)>5:
            # print(line)
            time = Time(file=line[0], type=line[1], text_start=int(line[2]), text_end=int(line[3]), text=line[4], answer=line[5].strip())
            times.append(time)
    parser = Parser()
    print(parser.parsers.keys())

    records = {
        'DATE': {
            'correct': 0,
            'wrong': 0,
            'error': 0,
        },
        'SET': {
            'correct': 0,
            'wrong': 0,
            'error': 0,
        },
        'DURATION': {
            'correct': 0,
            'wrong': 0,
            'error': 0,
        },
        'TIME': {
            'correct': 0,
            'wrong': 0,
            'error': 0,
        }
    }

    for t in times:
        # parse_type = -1

        try:
            if t.type in parser.parsers.keys():
                ans = parser.parse(t.text, t.type)
            else:
                continue          

            # print(f'{t.file} \t {t.type} \t {t.text_start} \t {t.text_end} \t {t.text:20} \t -> \t {ans} \t {t.answer} \t {"CORRECT" if ans == t.answer else "WRONG"}')

            if ans == t.answer: 
                records[t.type]['correct'] += 1
            else:
                records[t.type]['wrong'] += 1
                # print_log(t, ans)

                
        except Exception as e:
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            # print(errMsg)
            # # print(f"{t.text} \t {t.answer} \t {parse_type}")
            # print()
            records[t.type]['error'] += 1
            
            print_log(t, ans, is_error=True)
        finally:
            pass

    for r in records.keys():
        if (records[r]['correct'] + records[r]['wrong'] + records[r]['error']) == 0:
            print(f"{r:10} \t CORRECT: {records[r]['correct']} \t WRONG: {records[r]['wrong']} \t ERROR: {records[r]['error']} \t ACC: {0} F1: {0}")
        else:
            print(f"{r:10} \t CORRECT: {records[r]['correct']} \t WRONG: {records[r]['wrong']} \t ERROR: {records[r]['error']} \t ACC: {records[r]['correct'] / (records[r]['correct'] + records[r]['wrong'] + records[r]['error'])} F1: {2 * records[r]['correct'] / (2 * records[r]['correct'] + records[r]['wrong'] + records[r]['error'])}")

    print(f"correct: {sum([records[t]['correct'] for t in records.keys()])}")
    print(f"wrong: {sum([records[t]['wrong'] for t in records.keys()])}")
    print(f"acc: {sum([records[t]['correct'] for t in records.keys()]) / (sum([records[t]['correct'] for t in records.keys()]) + sum([records[t]['wrong'] for t in records.keys()]) + sum([records[t]['error'] for t in records.keys()]) )}")
    f1_score = 2 * sum([records[t]['correct'] for t in records.keys()]) / (2 * sum([records[t]['correct'] for t in records.keys()]) + sum([records[t]['wrong'] for t in records.keys()]) + sum([records[t]['error'] for t in records.keys()]))
    print(f"f1_score: {f1_score}")


if __name__ == '__main__':
    main()