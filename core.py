import sys
import file_utils
import apk_utils
import config_utils
import log_utils
import os
import os.path
import time

def pack(game, channel, sourcepath, isPublic):
    sourcepath = sourcepath.replace('\\', '/')
    if not os.path.exists(sourcepath):
        return 1
    appID = game['appID']
    appKey = game['appKey']
    appName = game['appName']
    appDescri = game['appDesc']
    channelId = channel['id']
    channelName = channel['name']
    sdkName = channel['sdk']
    log_utils.info('APPName: is %s ', appName)
    if 'YHGameName' in channel:
        channelMyName = channel['YHGameName']
        log_utils.info('channelName: %s ', channelName)
        log_utils.info('channelMyName: %s ', channelMyName)
    log_utils.info('appID: %s ', appID)
    log_utils.info('appName: %s ', appName)
    log_utils.info('appDescript: %s ', appDescri)
    log_utils.info('channelName: %s ', channelName)
    log_utils.info('APPName: %s ', '-------------------------')
    workDir = 'workspace/' + appName + '/' + sdkName
    workDir = file_utils.getFullPath(workDir)
    file_utils.del_file_folder(workDir)
    tempApkSource = workDir + '/temp.apk'
    file_utils.copy_file(sourcepath, tempApkSource)
    decompileDir = workDir + '/decompile'
    ret = apk_utils.decompileApk(tempApkSource, decompileDir)
    if ret:
        return 1
    sdkSourceDir = file_utils.getFullPath('config/sdk/' + sdkName)
    smaliDir = decompileDir + '/smali'
    sdkDestDir = workDir + '/sdk/' + sdkName
    file_utils.copy_files(sdkSourceDir, sdkDestDir)
    if not os.path.exists(sdkSourceDir + '/classes.dex'):
        apk_utils.jar2dex(sdkSourceDir, sdkDestDir)
    sdkDexFile = sdkDestDir + '/classes.dex'
    ret = apk_utils.dex2smali(sdkDexFile, smaliDir, 'baksmali.jar')
    if ret:
        return 1
    newPackageName = apk_utils.renamePackageName(channel, decompileDir, channel['suffix'], isPublic)
    ret = apk_utils.handleThirdPlugins(workDir, decompileDir, game, channel, newPackageName)
    if ret:
        return 1
    ret = apk_utils.copyResource(game, channel, newPackageName, sdkDestDir, decompileDir, channel['operations'], channelName)
    if ret:
        return 1
    ret = apk_utils.copyChannelResources(game, channel, decompileDir)
    if ret:
        return 1
    apk_utils.copyAppResources(game, decompileDir)
    apk_utils.copyAppRootResources(game, decompileDir)
    apk_utils.appendChannelIconMark(game, channel, decompileDir)
    apk_utils.writeDevelopInfo(appID, appKey, channel, decompileDir)
    apk_utils.writePluginInfo(channel, decompileDir)
    apk_utils.writeManifestMetaInfo(channel, decompileDir)
    apk_utils.modifyGameName(channel, decompileDir)
    apk_utils.editActivityName(channel, decompileDir)
    apk_utils.editMainActivity(decompileDir)
    ret = apk_utils.doSDKScript(channel, decompileDir, newPackageName, sdkDestDir)
    if ret:
        return 1
    ret = apk_utils.doGamePostScript(game, channel, decompileDir, newPackageName)
    if ret:
        return 1
    ret = apk_utils.addSplashScreen(workDir, channel, decompileDir)
    if ret:
        return 1
    ret = apk_utils.generateNewRFile(newPackageName, decompileDir)
    if ret:
        return 1
    targetApk = workDir + '/output.apk'
    XMLPath = ''
    ret = apk_utils.recompileApk(XMLPath, decompileDir, targetApk)
    if ret:
        return 1
    apk_utils.copyRootResFiles(targetApk, decompileDir)
    ret = apk_utils.signApk(appName, channelId, targetApk)
    if ret:
        return 1
    channelNameStr = channelName.replace(' ', '')
    if isPublic:
        destApkName = channelNameStr + '-' + time.strftime('%Y%m%d%H') + '.apk'
    else:
        destApkName = channelNameStr + '-' + time.strftime('%Y%m%d%H') + '-debug.apk'
    destApkPath = file_utils.getFullOutputPath(appName, channelName, appDescri)
    openPaths = file_utils.getFullOutputOpensPath(appName, channelName, appDescri)
    destApkPath = os.path.join(destApkPath, destApkName)
    ret = apk_utils.alignApk(targetApk, destApkPath)
    if ret:
        return 1
    log_utils.info('-------------------------------------------\n')
    log_utils.info('channel %s package success. \n\t\t ==>>>> APK Path: %s', channelName, destApkPath)
    log_utils.info('-------------------------------------------\n %s', '"' + openPaths + '"')
    os.system('start "" "' + openPaths + '"')
    log_utils.info('-------------------------------------------\n')
    return 0

