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

def read_file(file_name):
    with open(file_name, 'r', encoding="UTF-8") as f:
        lines = f.readlines()
        result = map(lambda x: x.split('\t'), lines)
        return list(result)
    
def save_data(file_name, data):
    with open(file_name, 'w') as f:
        for line in data:
            f.write(line)

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
    results = []

    times = []
    for line in data:
        if line == ['\n'] or line == [''] or line == ['\r\n'] or line == ['\r'] or line == ['\n']:
            continue
        # print(line)
        time = Time(file=line[0], type=line[1], text_start=int(line[2]), text_end=int(line[3]), text=line[4].strip())
        times.append(time)
    parser = Parser()
    # print(parser.parsers.keys())

    for t in times:
        # parse_type = -1

        try:
            if t.type in parser.parsers.keys():
                ans = parser.parse(t.text, t.type)
                if ans == (None, None, None):
                    results.append([t.file, t.type, t.text_start, t.text_end, t.text])
                    # results.append(f"{t.file}\t{t.type}\t{t.text_start}\t{t.text_end}\t{t.text}\n")
                else:
                    results.append([t.file, t.type, t.text_start, t.text_end, t.text, ans])
                    # results.append(f"{t.file}\t{t.type}\t{t.text_start}\t{t.text_end}\t{t.text}\t{ans}\n")
 
            else:
                results.append([t.file, t.type, t.text_start, t.text_end, t.text])
                # results.append(f"{t.file}\t{t.type}\t{t.text_start}\t{t.text_end}\t{t.text}\n")
    
                
        except Exception as e:
            # print('err')
            error_class = e.__class__.__name__ #取得錯誤類型
            detail = e.args[0] #取得詳細內容
            cl, exc, tb = sys.exc_info() #取得Call Stack
            lastCallStack = traceback.extract_tb(tb)[-1] #取得Call Stack的最後一筆資料
            fileName = lastCallStack[0] #取得發生的檔案名稱
            lineNum = lastCallStack[1] #取得發生的行號
            funcName = lastCallStack[2] #取得發生的函數名稱
            errMsg = "File \"{}\", line {}, in {}: [{}] {}".format(fileName, lineNum, funcName, error_class, detail)
            print(errMsg)
            # # print(f"{t.text} \t {t.answer} \t {parse_type}")
            # print()
            if t.text != 'at' and t.text != '/' and len(t.text) > 1:
                print(f"{t.file}\t{t.type}\t{t.text_start}\t{t.text_end}\t{t.text}\n")
            # results.append(f"{t.file}\t{t.type}\t{t.text_start}\t{t.text_end}\t{t.text}\n")
        finally:
            # print('finally')
            pass
    save_file_name = file_name.split('.')[0] + '_result_sorted.txt'
    results = sorted(results, key=lambda x: (x[0], x[2], x[3]))
    results = map(lambda x: '\t'.join(map(lambda y: str(y), x)) + '\n', results)
                     
    save_data(save_file_name, results)
    # print(results)
    print('done')


if __name__ == '__main__':
    main()