import os
import requests
import json


def data_reader(name):
    resp = requests.get(
        "https://raw.githubusercontent.com/v2ray/domain-list-community/master/data/"+name).content.decode('utf-8')
    data_list = resp.split("\n")

    # 删除空白行
    data_list = [x for x in data_list if x != '']
    # 删除注释行
    data_list = [x for x in data_list if x[0] != '#']
    #忽略空格后的内容
    data_list = [x.split(" ")[0] for x in data_list]
    #递归读取 include 指向的文件
    for item in data_list:
        if item[0:8] == "include:":
            data_list = data_list + data_reader(item[8:])
    #删除 include 行
    data_list = [x for x in data_list if x[0:8] != "include:"]

    return data_list


def data_parser_qx(data_list, name, app_name):
    print(name)
    try:
        os.mkdir(app_name)
        os.chdir(app_name)
    except FileExistsError:
        os.chdir(app_name)
    data_list = [x for x in data_list if x[0:6] != "regex:"]
    filter_list = []
    for item in data_list:
        if item[0:5] == "full:":
            filter_list.append("host, " + item[5:] + ", " + name)
        elif item[0:] == "keyword:":
            filter_list.append("host-keyword, " + item + ", " + name)
        else:
            filter_list.append("host-suffix, " + item + ", " + name)
    with open(name, "w", encoding="utf-8") as e:
        for item in filter_list:
            print(item)
            e.write(item+"\n")
    os.chdir('../')


if __name__ == '__main__':
    file_list = []
    for domain_file in json.loads(requests.get("https://api.github.com/repos/v2ray/domain-list-community/contents/data/").content.decode("utf-8")):
        file_list.append(domain_file["name"])
    for name in file_list:
        data_list = data_reader(name)
        data_parser_qx(data_list,name,"quantumult-x")
# datalist = data_reader("mozilla")
# data_parser_qx(datalist,"mozilla")
