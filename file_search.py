# 2017.01.16 18:53:44 中国标准时间
#Embedded file name: F:\YinHuSDK\tools\U8SDKTool-Win-P34\scripts\file_search.py
import sys
import os
import os.path
import file_utils
import log_utils

def printPats(level, path, picName):
    allFileNum = 0
    fileNameV4 = 'icon.png'
    dirList = []
    fileList = []
    files = os.listdir(path)
    dirList.append(str(level))
    for f in files:
        if os.path.isdir(path + '/' + f):
            if f[0] == '.':
                pass
            else:
                dirList.append(f)
        if os.path.isfile(path + '/' + f):
            fileNameV4 = f
            log_utils.warning('AA %s-->', fileNameV4)
            if fileNameV4 == picName + '.png':
                log_utils.warning('BB %s----->', path + '/' + f)
                os.remove(path + '/' + f)
            fileList.append(f)

    i_dl = 0
    for dl in dirList:
        if i_dl == 0:
            i_dl = i_dl + 1
        else:
            print '-' * int(dirList[0]), dl
            printPath(int(dirList[0]) + 1, path + '/' + dl)

    for fl in fileList:
        print '-' * int(dirList[0]), fl
        allFileNum = allFileNum + 1

    return fileNameV4

# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.01.16 18:53:44 中国标准时间
