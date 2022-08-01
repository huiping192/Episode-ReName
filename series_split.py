import os
import argparse
import shutil
import re

# from loguru import logger

target_path = ''
rule_path = ''

ap = argparse.ArgumentParser()
ap.add_argument('--path', required=True, help='目标路径')
ap.add_argument('--rule', required=True, help='spilt rule')

args = vars(ap.parse_args())
target_path = args['path']
rule_path = args['rule']


def loop_dic(dic_path):
    for file_name in os.listdir(dic_path):
        path = os.path.join(dic_path, file_name)
        if os.path.isfile(path):
            rename_file(path)


def get_season_ep(index):
    return get_real_season_ep(1,0,index)

def get_real_season_ep(season, count, index):
    if season > len(rule_dic.keys()):
        return None,None
    season_ep_count = int(rule_dic[str(season)])
    print("season_ep_count", season, season_ep_count)
    season_ep_max = count + season_ep_count
    print("season_ep_max", season_ep_max)
    ep = index - count
    if index <= season_ep_max:
        return season, ep
    else:
        return get_real_season_ep(season+1, season_ep_max ,index)


def find_file_index(path):
    file_name = os.path.basename(path)
    ex = os.path.splitext(file_name)
    file_name = ex[0]
    print("file name:", file_name)

    pat = '(\d{1,4})'
    res = re.findall(pat, file_name)
    if res:
        print("res",res)
        return int(res[0].strip())

def rename_file(path):
    index = find_file_index(path)
    if not index:
        return
    print("index:", index)
    season, ep = get_season_ep(index)
    if not season:
        return
    if not ep:
        return
    print("season, ep:", season, ep)

    dic_path = os.path.dirname(path)
    ex = os.path.splitext(path)
    file_ex = ex[1]
    if not file_ex:
        return

    season_str = get_int_str(season)
    ep_str = get_int_str(ep)

    file_name = "S" + season_str + "E" + ep_str + file_ex
    new =  os.path.join(dic_path, file_name)
    print("new:", new)

    os.rename(path, new)

def get_int_str(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)

def parse_rule_file():
    file_path = rule_path
    if not file_path:
        return {}
    dic = {}

    f = open(file_path, 'r', encoding='UTF-8')

    datalist = f.readlines()
    for line in datalist:
        array = line.strip().split(',')
        dic[array[0]] = array[1]

    f.close()

    return dic


rule_dic = parse_rule_file()
print("rule",rule_dic)
loop_dic(target_path)