# 2017.01.16 18:55:47 中国标准时间
#Embedded file name: F:\YinHuSDK\tools\U8SDKTool-Win-P34\scripts\main.py
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
    tip = u'**********\u5f53\u524d\u914d\u7f6e\u7684\u6e20\u9053\u53f7**********'
    print tip
    chStrFormat = u'\t\u6e20\u9053\u53f7 \t\t \u6e20\u9053\u540d \n'
    print chStrFormat
    appName = game['appName']
    channels = config_utils.getAllChannels(appName, isPublic)
    if channels != None and len(channels) > 0:
        for ch in channels:
            chStr = u'\t%s \t\t %s ' % (ch['id'], ch['name'])
            print chStr

    tip = u'\nSelect channels(input channelID, comma split)\n\t \u8bf7\u8f93\u5165\u6e20\u9053\u53f7 (0\u4f4d\u5168\u90e8 \u591a\u6e20\u9053\u53ef\u4f7f\u7528 \uff0c\u9017\u53f7\u5206\u9694) :  '
    inputChannels = input(tip)
    inputChannels = str(inputChannels)
    inputChannels = inputChannels.encode('utf-8')
    print u'\n'
    print u'\t>>>>>>>>>>>>>>>>>> ROOT\u673a\u5668\u4eba \u5373\u5c06\u4e3a\u60a8\u6253\u5305  '
    print u'\n'
    if inputChannels == '0':
        print u'\t>>>>>>>>>>>>>>>>>> \u6240\u6709\u6e20\u9053\u6253\u5305'
        packAllChannels(game, channels, isPublic)
    else:
        lstChannels = inputChannels.replace('(', '').replace(')', '').replace(' ', '').split(',')
        print u'\t>>>>>>>>>>>>>>>>>> \u5206\u53d1\u6e20\u9053\u6253\u5305\n'
        packSelectedChannels(game, channels, lstChannels, isPublic)


def packAllChannels(game, channels, isPublic):
    basePath = file_utils.getCurrDir()
    log_utils.info('Curr Work Dir::%s', basePath)
    if channels != None and len(channels) > 0:
        clen = len(channels)
        log_utils.info('Now Have %s channels to package', clen)
        packagePath = file_utils.getFullPath('yinhu.apk')
        log_utils.info('The base apk file is :%s', packagePath)
        if not os.path.exists(packagePath):
            log_utils.error("The apk file name must be 'yinhu.apk'")
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
    if selectedChannels == None or len(selectedChannels) <= 0:
        print 'the selected channels is none or empty'
        return
    basePath = file_utils.getCurrDir()
    log_utils.info('Curr Work Dir::%s', basePath)
    if channels != None and len(channels) > 0:
        clen = len(selectedChannels)
        log_utils.info('Now Have %s channels to package ', clen)
        packagePath = file_utils.getFullPath('yinhu.apk')
        log_utils.info('The base apk file is : %s', packagePath)
        if not os.path.exists(packagePath):
            log_utils.error("The apk file name must be 'yinhu.apk'")
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

# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.01.16 18:55:47 中国标准时间
