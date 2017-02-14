# -*- coding: utf-8 -*-
import sys
import core
import file_utils
import apk_utils
import config_utils
import file_search
import os
import os.path
import time
import log_utils
try:
    input = raw_input
except NameError:
    pass

def main(game, isPublic, isFullRes = False):
    tip = u'\n====================== 游戏已配置的渠道 ============================\n'
    print tip
    chStrFormat = u'\t\t渠道号 \t\t\t 渠道名 \n'
    print chStrFormat
    appName = game['appName']
    channels = config_utils.getAllChannels(appName, isPublic)
    if channels != None and len(channels) > 0:
        for ch in channels:
            chStr = u'\t\t%s \t\t\t %s \n' % (ch['id'], ch['name'])
            print chStr

    tip = u'请输入要打包的渠道号(0：打包所有渠道， 多个渠道可使用","逗号分隔):  '
    inputChannels = input(tip)
    inputChannels = str(inputChannels)
    inputChannels = inputChannels.encode('utf-8')
    print u'\n'
    if inputChannels == '0':
        print u'\t......打包所有已配置的渠道......\n'
        packAllChannels(game, channels, isPublic)
    else:
        lstChannels = inputChannels.replace('(', '').replace(')', '').replace(' ', '').split(',')
        print u'\t......打包指定的渠道.......\n'
        packSelectedChannels(game, channels, lstChannels, isPublic)


def packAllChannels(game, channels, isPublic):
    basePath = file_utils.getCurrDir()
    log_utils.info('Current Work Dir: %s', basePath)
    if channels != None and len(channels) > 0:
        clen = len(channels)
        log_utils.info('Now Have %s channels to package...', clen)
        packagePath = file_utils.getFullPath('rh.apk')
        log_utils.info('The base apk file is: %s', packagePath)
        if not os.path.exists(packagePath):
            log_utils.error("The apk file name must be 'rh.apk'")
            return
        sucNum = 0
        falNum = 0
        for channel in channels:
            ret = core.pack(game, channel, packagePath, isPublic)
            if ret:
                falNum = falNum + 1
            else:
                sucNum = sucNum + 1

        log_utils.info('<< all nice done >>')
        log_utils.info('<< success num:%s; fail num:%s>>', sucNum, falNum)


def packSelectedChannels(game, channels, selectedChannels, isPublic):
    '''
     将游戏打包指定的渠道
    :param game: 游戏信息
    :param channels: 所有配置的渠道
    :param selectedChannels:  选择的渠道
    :param isPublic: 是否正式包
    :return: 无
    '''
    if selectedChannels == None or len(selectedChannels) <= 0:
        print 'the selected channels is none or empty'
        return
    basePath = file_utils.getCurrDir()
    log_utils.info('Current Work Dir: %s', basePath)
    if channels != None and len(channels) > 0:
        clen = len(selectedChannels)
        log_utils.info('Now Have %s channels to package...', clen)
        packagePath = file_utils.getFullPath('rh.apk')
        log_utils.info('The base apk file is: %s', packagePath)
        if not os.path.exists(packagePath):
            log_utils.error("The apk file name must be 'rh.apk'")
            return
        sucNum = 0
        falNum = 0
        for channel in channels:
            channelId = channel['id']
            if channelId not in selectedChannels:
                continue
            ret = core.pack(game, channel, packagePath, isPublic)
            if ret:
                falNum = falNum + 1
            else:
                sucNum = sucNum + 1

        log_utils.info('<< all nice done >>')
        log_utils.info('<< success num:%s; fail num:%s>>', sucNum, falNum)