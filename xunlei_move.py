import os
import argparse
import shutil

# from loguru import logger

target_path = ''
save_path = ''

ap = argparse.ArgumentParser()
ap.add_argument('--path', required=True, help='目标路径')
ap.add_argument('--save', required=False, help='保存目标路径')

args = vars(ap.parse_args())
target_path = args['path']
save_path = args['save']

COMMON_MEDIA_EXTS = [
    '.flv',
    '.mkv',
    '.mp4',
    '.avi',
    '.rmvb',
    '.m2ts',
    '.wmv',
    '.webm',
]

exts = COMMON_MEDIA_EXTS

def loop_dic(dic_path):
    for file_name in os.listdir(dic_path):
        path = os.path.join(dic_path, file_name)
        if os.path.isfile(path):
            # logger.info(f"{'find file', path}")
            print("find file ", path)
            move_if_needed(path)
        elif os.path.isdir(path):
            # logger.info(f"{'find dic', path}")
            print("find dic ", path)
            move_dic_if_needed(path)


def should_move_dic(dic_path):
    for file_name in os.listdir(dic_path):
        path = os.path.join(dic_path, file_name)
        if os.path.isfile(path):
            print("find sub file ", path)
            if ".xltd" in file_name:
                return False
        elif os.path.isdir(path):
            # logger.info(f"{'find dic', path}")
            print("find sub dic ", path)
            if not should_move_dic(path):
                return False
    return True

def move_dic_if_needed(path):
    if should_move_dic(path):
        print("move dic", path)
        shutil.move(path, save_path)

def move_if_needed(file_path):
    file_name = os.path.basename(file_path)
    ext = os.path.splitext(file_name)[1].lower()
    if not ext in exts:
        print("ext no match.")
        return False
    if os.path.getsize(file_path) > 80 * 1024 * 1024:
        move_file(file_path)


def move_file(file_path):
    file_name = os.path.basename(file_path)

    new = os.path.join(save_path, file_name)
    # logger.info(f"{'new path', new}")
    print("new path ", new)

    if os.path.exists(new):
        os.remove(new)

    shutil.move(file_path, save_path)
    print("move path done", new)
    # logger.info(f"{'move path done', new}")


loop_dic(target_path)
