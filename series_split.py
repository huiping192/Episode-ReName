import os
import argparse
import shutil
import re

# from loguru import logger

target_path = ''
rule_path = ''

COMMON_MEDIA_EXTS = [
    '.flv',
    '.mkv',
    '.mp4',
    '.avi',
    '.rmvb',
    '.m2ts',
    '.wmv',
]

# 字幕文件
COMMON_CAPTION_EXTS = [
    '.srt',
    '.ass',
    '.ssa',
    '.sub',
    '.smi',
]

exts = COMMON_MEDIA_EXTS + COMMON_CAPTION_EXTS

ap = argparse.ArgumentParser()
ap.add_argument('--path', required=True, help='目标路径')

args = vars(ap.parse_args())
target_path = args['path']

def loop_dic(dic_path):
    for file_name in os.listdir(dic_path):
        path = os.path.join(dic_path, file_name)
        if os.path.isfile(path):
            if need_process_file(path):
                rename_file(path)
            else:
                print("skip file",path)

def need_process_file(path):
    file_name = os.path.basename(path)

    ext = os.path.splitext(file_name)[1].lower()
    if not ext in exts:
        print("false1")
        return False

    pat = '[Ss](\d{1,4})[Ee](\d{1,4}(\.5)?)'
    res = re.match(pat, file_name)
    if res:
        season = res[1]
        print("season", season)
        if season == 1:
            return True
        else:
            return False
    else:
        print("false")
        return True

def find_file_index(path):
    file_name = os.path.basename(path)
    ex = os.path.splitext(file_name)
    file_name = ex[0]
    print("file name:", file_name)

    pat = '[Ss](\d{1,4})[Ee](\d{1,4}(\.5)?)'
    res = re.findall(pat, file_name)
    if res:
        print("res haha",res)
        season, ep = res[0][0], res[0][1]
        if int(season.strip()) == 1:
            return int(ep.strip())

    pat = '(\d{1,4})'
    res = re.findall(pat, file_name)
    if res:
        print("res",res)
        return int(res[0].strip())

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

    series = os.path.basename(os.path.dirname(path))

    dic_path = os.path.dirname(path)
    ex = path.split('.', 1)
    file_ex = ex[1]
    if not file_ex:
        return

    season_str = get_int_str(season)
    ep_str = get_int_str(ep)

    file_name = series + " S" + season_str + "E" + ep_str + "." + file_ex
    new =  os.path.join(dic_path, file_name)
    print("new:", new)

    os.rename(path, new)

def get_int_str(num):
    return str(int(num)).zfill(2)

def parse_rule_file():
    file_path = os.path.join(target_path,"rule.txt")
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