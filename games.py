# -*- coding: utf-8 -*-
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
    tip = u'\n========================== 已添加的游戏 =================================\n'
    log_utils.info('Current YinHuSDK Version: %s', sdkVersion)
    print tip
    print '------------------------------------------------------------------------'
    chStrFormat = u'编号\t\tappID\t\t游戏文件夹\t\t游戏名称\n'
    print chStrFormat
    pent = 0
    #获取所有配置的游戏
    games = config_utils.getAllGames()
    if games != None and len(games) > 0:
        for ch in games:
            chStr = u' %s\t\t%s\t\t%s\t\t%s\n' % (pent,
                                                  ch['appID'],
                                                  ch['appName'],
                                                  ch['appDesc'])
            print chStr
            pent = pent + 1

    print '------------------------------------------------------------------------'
    tip = '\nSelect Game(appID): '
    selectedGameID = input(tip)
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
