import os
import time
import sys

def modified_within(top, seconds):
    now = time.time()
    print os.walk(top).next()
    for path, dirs, files in os.walk(top):
        # print '=>', path, dirs, files
        for name in files:
            fullpath = os.path.join(path, name)
            if os.path.exists(fullpath):
                mtime = os.path.getmtime(fullpath)
                print mtime
                sys.exit()

                if mtime > (now - seconds):
                    print(fullpath)
modified_within('/Users/zhutingting/Documents/zcy/awesome-script/src/data_catch', 10000)