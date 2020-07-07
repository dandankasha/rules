import json
import os
import sys

import requests


def data_reader(name):
    resp = requests.get(
        "https://raw.githubusercontent.com/v2ray/domain-list-community/master/data/"+name).content.decode('utf-8')
    domain_list = resp.split("\n")

    # 删除空白行
    domain_list = [x for x in domain_list if x != '']
    # 删除注释行
    domain_list = [x for x in domain_list if x[0] != '#']
    # 忽略空格后的内容
    domain_list = [x.split(" ")[0] for x in domain_list]
    # 递归读取 include 指向的文件
    for item in domain_list:
        if item[0:8] == "include:":
            domain_list = domain_list + data_reader(item[8:])
    # 删除 include 行
    domain_list = [x for x in domain_list if x[0:8] != "include:"]

    return domain_list


def data_parser_qx(domain_list, name):
    print(name)
    try:
        os.mkdir("quantumult-x")
        os.chdir("quantumult-x")
    except FileExistsError:
        os.chdir("quantumult-x")
    domain_list = [x for x in domain_list if x[0:6] != "regex:"]
    filter_list = []
    for item in domain_list:
        if item[0:5] == "full:":
            filter_list.append("host, " + item[5:] + ", " + name)
        elif item[0:] == "keyword:":
            filter_list.append("host-keyword, " + item[8:] + ", " + name)
        else:
            filter_list.append("host-suffix, " + item + ", " + name)
    with open(name, "w", encoding="utf-8") as e:
        for item in filter_list:
            print(item)
            e.write(item+"\n")
    os.chdir('../')


def data_parser_clash_prem(domain_list, name):
    print(name)
    try:
        os.mkdir("clash-premium")
        os.chdir("clash-premium")
    except FileExistsError:
        os.chdir("clash-premium")
    domain_list = [x for x in domain_list if x[0:6] != "regex:"]
    filter_list = []
    for item in domain_list:
        if item[0:5] == "full:":
            filter_list.append("DOMAIN," + item[5:])
        elif item[0:] == "keyword:":
            filter_list.append("DOMAIN-KEYWORD," + item[8:])
        else:
            filter_list.append("DOMAIN-SUFFIX," + item)
    with open(name, "w", encoding="utf-8") as e:
        e.write("payload:\n")
        for item in filter_list:
            print(item)
            e.write("  - "+item+"\n")
    os.chdir('../')


if __name__ == '__main__':
    app_name = sys.argv[1]
    if app_name == "qx":
        path_name = "quantumult-x/"
        if os.path.exists(path_name):
            [os.remove(path_name+x) for x in os.listdir(path_name)]
    elif app_name == "clash-prem":
        path_name = "clash-premium/"
        if os.path.exists(path_name):
            [os.remove(path_name+x) for x in os.listdir(path_name)]
    for domain_file in json.loads(requests.get("https://api.github.com/repos/v2ray/domain-list-community/contents/data/").content.decode("utf-8")):
        domain_list = data_reader(domain_file["name"])
        if app_name == "qx":
            data_parser_qx(domain_list, domain_file["name"])
        elif app_name == "clash-prem":
            data_parser_clash_prem(domain_list, domain_file["name"])
