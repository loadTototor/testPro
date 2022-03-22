import json
import os


def write_to_json(filepath, filename, dic):
    filePath = os.path.join(os.getcwd(), filepath)
    if not os.path.exists(filePath):
        os.mkdir(filePath)

    with open(filePath + os.sep + filename, 'w') as f:
        json.dump(dic, f)

def read_get_json(filepath, filename):
    with open(filepath + os.sep + filename, 'r', encoding='utf-8') as f:
        rdic = json.load(f)

    return rdic


if __name__ == '__main__':
    filepath = os.getcwd()
    filename = 'test.json'
    dic = {'name': 'zhangsan', 'age': '20'}

    write_to_json(filepath, filename, dic)

    a = read_get_json(filepath, filename)
    print(a)
    print(type(a))
