import os
import time


def file_change(fold_path, change_time):
    # get changed file path
    last_time = read_file()
    for path, dirs, files in os.walk(fold_path):
    # print '=>', path, dirs, files
        for name in files:
            fullpath = os.path.join(path, name)
            if os.path.exists(fullpath):
                mtime = os.path.getmtime(fullpath)
                if mtime > (now - seconds):
                    print(fullpath)

    pass

def data_change(file_name):
    pass


def read_file(file_name):
    with open(file_name, 'r') as f:
        return f.readline()

def write_file(file_name, content):
    with open(file_name, 'w+') as f:
        f.write(content)

