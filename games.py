# 2017.01.16 18:54:27 中国标准时间
#Embedded file name: F:\YinHuSDK\tools\U8SDKTool-Win-P34\scripts\games.py
import sys
import core
import file_utils
import apk_utils
import config_utils
import log_utils
import os
import os.path
import time
import main
import main_thread
try:
    input = raw_input
except NameError:
    pass

def entry(isPublic, isSelectable, threadNum, sdkVersion):
    log_utils.info('Curr Python Version: %s', config_utils.get_py_version())
    tip = u'\n\t ***********************************\u6240\u6709\u6e38\u620f***********************************'
    log_utils.info('Current YinHuSDK Version: %s', sdkVersion)
    print tip
    chStrFormat = u'\t --appID-- \t\t --\u6e38\u620f\u6587\u4ef6\u5939-- \t\t ----\u6e38\u620f\u540d\u79f0---- \n\n'
    print chStrFormat
    pent = 0
    games = config_utils.getAllGames()
    if games != None and len(games) > 0:
        for ch in games:
            chStr = u'%s\t %s \t\t %s -------------------\t%s' % (pent,
             ch['appID'],
             ch['appName'],
             ch['appDesc'])
            print chStr
            if pent == 0:
                print ''
            elif pent % 10 == 0 and pent != 1:
                print ''
            pent = pent + 1

    tip = '\n\tSelect Game(appID): '
    selectedGameID = input(tip)
    selectedGameID = str('1087' + selectedGameID)
    log_utils.info('Current Selected Game ID is : %s ', selectedGameID)
    game = getGameByAppID(selectedGameID, games)
    gameDescs = game['appDesc']
    log_utils.info('Current Selected Game Name is : %s ', gameDescs)
    if isSelectable:
        main.main(game, isPublic)
    else:
        main_thread.main(game, isPublic, threadNum)


def getGameByAppID(appID, games):
    if games == None or len(games) <= 0:
        return
    for game in games:
        if game['appID'] == appID:
            return game

# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.01.16 18:54:27 中国标准时间
