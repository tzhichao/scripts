# -*- coding:utf-8 -*-
import file_utils
import os
import os.path
import config_utils
import smali_utils
import file_search
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree
import os
import os.path
import zipfile
import re
import subprocess
import platform
import log_utils
from xml.dom import minidom
import codecs
import sys
import time
import times_main
from PIL import Image
import image_utils
androidNS = 'http://schemas.android.com/apk/res/android'

def modifyGameName(channel, decompileDir):

    log_utils.info('\n\t')
    log_utils.info('============modifyGameName============')
    if 'RHGameName' not in channel:
        return
    gameName = channel['RHGameName']
    if gameName == None or len(gameName) == 0:
        return
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    labelKey = '{' + androidNS + '}label'
    applicationNode = root.find('application')
    applicationNode.set(labelKey, gameName)
    log_utils.info('modifyGameName : RHGameName is %s', gameName)
    log_utils.info('============modifyGameName Success============')
    log_utils.info('\n\t')
    tree.write(manifestFile, 'UTF-8')


def editActivityName(channel, decompileDir):
    log_utils.info('\n\t')
    log_utils.info('============editActivityName============')
    if 'RHGameName' not in channel:
        return
    gameName = channel['RHGameName']
    if gameName == None or len(gameName) == 0:
        return
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'
    labelKey = '{' + androidNS + '}label'
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    applicationNode = root.find('application')
    if applicationNode is None:
        return
    activityNodeLst = applicationNode.findall('activity')
    if activityNodeLst is None:
        return
    activityName = ''
    for activityNode in activityNodeLst:
        bMain = False
        intentNodeLst = activityNode.findall('intent-filter')
        if intentNodeLst is None:
            break
        for intentNode in intentNodeLst:
            bFindAction = False
            bFindCategory = False
            actionNodeLst = intentNode.findall('action')
            if actionNodeLst is None:
                break
            for actionNode in actionNodeLst:
                if actionNode.attrib[key] == 'android.intent.action.MAIN':
                    bFindAction = True
                    break

            categoryNodeLst = intentNode.findall('category')
            if categoryNodeLst is None:
                break
            for categoryNode in categoryNodeLst:
                if categoryNode.attrib[key] == 'android.intent.category.LAUNCHER':
                    bFindCategory = True
                    break

            if bFindAction and bFindCategory:
                bMain = True
                break

        if bMain:
            activityName = activityNode.attrib[key]
            activityNode.set(labelKey, gameName)
            break

    tree.write(manifestFile, 'UTF-8')
    log_utils.info('modifyGameName : RHGameName is %s', gameName)
    log_utils.info('modifyGameName : activityName is %s', activityName)
    log_utils.info('============modifyActivityGameName Success============')
    log_utils.info('\n\t')


def editMainActivity(decompileDir):
    log_utils.info('\n\t')
    log_utils.info('===============editMainActivity START===============')
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'
    labelKey = '{' + androidNS + '}label'
    mLaunchModes = '{' + androidNS + '}launchMode'
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    applicationNode = root.find('application')
    if applicationNode is None:
        return
    activityNodeLst = applicationNode.findall('activity')
    if activityNodeLst is None:
        return
    activityName = ''
    activityNameYY = ''
    bMain = False
    for activityNode in activityNodeLst:
        intentNodeLst = activityNode.findall('intent-filter')
        if intentNodeLst is None:
            break
        for intentNode in intentNodeLst:
            bFindAction = False
            bFindCategory = False
            actionNodeLst = intentNode.findall('action')
            if actionNodeLst is None:
                break
            for actionNode in actionNodeLst:
                if actionNode.attrib[key] == 'android.intent.action.MAIN':
                    bFindAction = True
                    break

            categoryNodeLst = intentNode.findall('category')
            if categoryNodeLst is None:
                break
            for categoryNode in categoryNodeLst:
                if categoryNode.attrib[key] == 'android.intent.category.LAUNCHER':
                    bFindCategory = True
                    break

            if bFindAction and bFindCategory:
                bMain = True
                activityNode.set(mLaunchModes, 'singleTop')
                break



    appNode = root.find('application')
    activityNodes = appNode.findall('activity')
    if activityNodes != None and len(activityNodes) > 0:
        for activityNode in activityNodes:
            activityNameYY = activityNode.get(key)
            log_utils.info('*****activityName   :%s', activityNameYY)
            spName = 'com.junhai.dpcq.yinhu.LoadingActivity'
            if activityNameYY == spName:
                log_utils.info('editMainActivity EDIT MainActivity is:%s', activityNameYY)
                activityNode.set(mLaunchModes, 'singleTop')
            spName = 'com.junhai.dpcq.yinhu.FanRen'
            if activityNameYY == spName:
                log_utils.info('editMainActivity ADD MainActivity is:%s', activityNameYY)
                junhai_fanren_filter = SubElement(activityNode, 'intent-filter')
                actionNode = SubElement(junhai_fanren_filter, 'action')
                actionNode.set(key, 'android.intent.action.MAIN')
                categoryNode = SubElement(junhai_fanren_filter, 'category')
                categoryNode.set(key, 'android.intent.category.LAUNCHER')
                activityNode.set(mLaunchModes, 'singleTop')

    tree.write(manifestFile, 'UTF-8')
    log_utils.info('===============editMainActivity OVER===============')
    log_utils.info('\n\t')


def copyLibs(game, srcDir, dstDir):
    """
        copy shared libraries
    """
    if not os.path.exists(srcDir):
        return
    if not os.path.exists(dstDir):
        os.makedirs(dstDir)
    cpus = ['armeabi',
     'armeabi-v7a',
     'x86',
     'mips',
     'arm64-v8a',
     'x86_64']
    isfilter = 'cpuSupport' in game and len(game['cpuSupport']) > 0
    filters = None
    if isfilter:
        filters = game['cpuSupport'].split('|')
    openFlag = 10
    if openFlag == 100:
        for fucks in os.listdir(dstDir):
            sreFile = os.path.join(srcDir, fucks)
            deckFile = os.path.join(dstDir, fucks)
            if fucks == 'libtpnsWatchdog.so':
                if os.path.exists(deckFile):
                    log_utils.info('libtpnsWatchdog.so DEL--------->%s', deckFile)
                    os.remove(deckFile)
                else:
                    log_utils.warning('.so deckFile no exists--------->%s', deckFile)
            if fucks == 'libtpnsSecurity.so':
                if os.path.exists(deckFile):
                    log_utils.info('libtpnsSecurity.so DEL--------->%s', deckFile)
                    os.remove(deckFile)
                else:
                    log_utils.warning('.so deckFile no exists--------->%s \n\n', deckFile)
            if fucks == 'libWeGameSample.so':
                if os.path.exists(deckFile):
                    log_utils.info('libtpnsSecurity.so DEL--------->%s', deckFile)
                    os.remove(deckFile)
                else:
                    log_utils.warning('.so deckFile no exists--------->%s \n\n', deckFile)
            if fucks == 'libBugly.so':
                if os.path.exists(deckFile):
                    log_utils.info('libtpnsSecurity.so DEL--------->%s', deckFile)
                    os.remove(deckFile)
                else:
                    log_utils.warning('.so deckFile no exists--------->%s \n\n', deckFile)

    for f in os.listdir(srcDir):
        sourcefile = os.path.join(srcDir, f)
        targetfile = os.path.join(dstDir, f)
        if sourcefile.endswith('.jar'):
            continue
        if f in cpus and filters and f not in filters:
            continue
        if os.path.isfile(sourcefile):
            if not os.path.exists(targetfile) or os.path.getsize(targetfile) != os.path.getsize(sourcefile):
                destfilestream = open(targetfile, 'wb')
                sourcefilestream = open(sourcefile, 'rb')
                destfilestream.write(sourcefilestream.read())
                destfilestream.close()
                sourcefilestream.close()
        if os.path.isdir(sourcefile):
            log_utils.info('copyLibs sourcefile --------->%s', sourcefile)
            log_utils.info('copyLibs targetfile --------->%s', targetfile)
            copyLibs(game, sourcefile, targetfile)


def jar2dex(srcDir, dstDir, dextool = 'baksmali.jar'):
    """
        compile jar files to dex.
    """
    if platform.system() == 'Windows':
        dexToolPath = file_utils.getFullToolPath('dx.bat')
        cmd = '"%s" --dex --output="%s" ' % (dexToolPath, dstDir + '/classes.dex')
    else:
        dexToolPath = file_utils.getFullToolPath('/lib/dx.jar')
        cmd = file_utils.getJavaCMD() + ' -jar -Xms512m -Xmx512m "%s" --dex --output="%s" ' % (dexToolPath, dstDir + '/classes.dex')
    for f in os.listdir(srcDir):
        if f.endswith('.jar'):
            cmd = cmd + ' ' + os.path.join(srcDir, f)

    for f in os.listdir(os.path.join(srcDir, 'libs')):
        if f.endswith('.jar'):
            cmd = cmd + ' ' + os.path.join(srcDir, 'libs', f)

    ret = file_utils.execFormatCmd(cmd, 'jar2dex')


def dex2smali(dexFile, targetdir, dextool = 'baksmali.jar'):
    """
        Transfer the dex to smali.
    """
    if not os.path.exists(dexFile):
        log_utils.error('the dexfile is not exists. path:%s', dexFile)
        return
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    dexFile = file_utils.getFullPath(dexFile)
    smaliTool = file_utils.getFullToolPath(dextool)
    targetdir = file_utils.getFullPath(targetdir)
    cmd = '"%s" -jar "%s" -o "%s" "%s"' % (file_utils.getJavaCMD(),
     smaliTool,
     targetdir,
     dexFile)
    ret = file_utils.execFormatCmd(cmd, 'dex2smali')
    return ret


def decompileApk(source, targetdir, apktool = 'apktool2.jar'):
    """
        Decompile apk
    """
    apkfile = file_utils.getFullPath(source)
    targetdir = file_utils.getFullPath(targetdir)
    if os.path.exists(targetdir):
        file_utils.del_file_folder(targetdir)
    if not os.path.exists(targetdir):
        os.makedirs(targetdir)
    try:
        apktool = 'apktool2.jar'
        apktool = file_utils.getFullToolPath(apktool)
        cmd = '"%s" -jar -Xms512m -Xmx512m "%s" -q d -b -f "%s" -o "%s"' % (file_utils.getJavaCMD(),
         apktool,
         apkfile,
         targetdir)
        ret = file_utils.execFormatCmd(cmd, 'decompileApk')
        if ret == 1:
            apktool = 'apktool.jar'
            apktool = file_utils.getFullToolPath(apktool)
            cmd = '"%s" -jar -Xms512m -Xmx512m "%s" -q d -b -f "%s" -o "%s"' % (file_utils.getJavaCMD(),
             apktool,
             apkfile,
             targetdir)
            ret = file_utils.execFormatCmd(cmd, 'decompileApk')
    except BaseException as e:
        apktool = 'apktool.jar'
        apktool = file_utils.getFullToolPath(apktool)
        cmd = '"%s" -jar -Xms512m -Xmx512m "%s" -q d -b -f "%s" -o "%s"' % (file_utils.getJavaCMD(),
         apktool,
         apkfile,
         targetdir)
        ret = file_utils.execFormatCmd(cmd, 'decompileApk')
        log_utils.error('DecompileApk Exception: %s', e)
        raise e
    finally:
        log_utils.warning('********************')
        log_utils.warning('***')
        log_utils.warning('*** Use is : %s', apktool)
        log_utils.warning('***')
        log_utils.warning('********************')

    return ret


def recompileApk(XMLPath, sourcefolder, apkfile, apktool = 'apktool2.jar'):
    """
        Recompile apk
    """
    os.chdir(file_utils.curDir)
    sourcefolder = file_utils.getFullPath(sourcefolder)
    apkfile = file_utils.getFullPath(apkfile)
    apktool = file_utils.getFullToolPath(apktool)
    log_utils.info('Well loading go........')
    times = times_main.getTimes(XMLPath)
    time.sleep(int(times))
    log_utils.info('Well loading to........')
    reload(sys)
    sys.setdefaultencoding('gbk')
    ret = 1
    if os.path.exists(sourcefolder):
        try:
            apktool = 'apktool2.jar'
            apktool = file_utils.getFullToolPath(apktool)
            cmd = '"%s" -jar -Xms512m -Xmx512m "%s" -q b -f "%s" -o "%s"' % (file_utils.getJavaCMD(),
             apktool,
             sourcefolder,
             apkfile)
            ret = file_utils.execFormatCmd(cmd, 'recompileApk')
            if ret == 1:
                apktool = 'apktool.jar'
                apktool = file_utils.getFullToolPath(apktool)
                cmd = '"%s" -jar -Xms512m -Xmx512m "%s" -q b -f "%s" -o "%s"' % (file_utils.getJavaCMD(),
                 apktool,
                 sourcefolder,
                 apkfile)
                ret = file_utils.execFormatCmd(cmd, 'recompileApk')
        except Exception as e:
            apktool = 'apktool.jar'
            apktool = file_utils.getFullToolPath(apktool)
            cmd = '"%s" -jar -Xms512m -Xmx512m "%s" -q b -f "%s" -o "%s"' % (file_utils.getJavaCMD(),
             apktool,
             sourcefolder,
             apkfile)
            ret = file_utils.execFormatCmd(cmd, 'recompileApk')
            log_utils.error('RecompileApk Exception: %s', e)
            raise e

    return ret


def signApk(appName, channelId, apkfile):
    """
        Sign apk
    """
    keystore = config_utils.getKeystore(appName, channelId)
    log_utils.info('the keystore file is %s', keystore['keystore'])
    signApkInternal(apkfile, keystore['keystore'], keystore['password'], keystore['aliaskey'], keystore['aliaspwd'])


def signApkInternal(apkfile, keystore, password, alias, aliaspwd):
    if not os.path.exists(keystore):
        return 1
    apkfile = file_utils.getFullPath(apkfile)
    keystore = file_utils.getFullPath(keystore)
    aapt = file_utils.getFullToolPath('aapt')
    listcmd = '%s list %s' % (aapt, apkfile)
    output = os.popen(listcmd).read()
    for filename in output.split('\n'):
        if filename.find('META_INF') == 0:
            rmcmd = '"%s" remove "%s" "%s"' % (aapt, apkfile, filename)
            file_utils.execFormatCmd(rmcmd, 'aaptRemoveMetaInfo')

    signcmd = '"%sjarsigner" -keystore "%s" -storepass "%s" -keypass "%s" "%s" "%s" -sigalg SHA1withRSA -digestalg SHA1' % (file_utils.getJavaBinDir(),
     keystore,
     password,
     aliaspwd,
     apkfile,
     alias)
    ret = file_utils.execFormatCmd(signcmd, 'signApk')
    return ret


def copyRootResFiles(apkfile, decompileDir):
    apkfile = file_utils.getFullPath(apkfile)
    aapt = file_utils.getFullToolPath('aapt')
    decompileDir = file_utils.getFullPath(decompileDir)
    igoreFiles = ['AndroidManifest.xml',
     'apktool.yml',
     'smali',
     'res',
     'original',
     'lib',
     'build',
     'assets',
     'dujinyang']
    igoreFileFullPaths = []
    for ifile in igoreFiles:
        fullpath = os.path.join(decompileDir, ifile)
        igoreFileFullPaths.append(fullpath)

    addFiles = []
    addFiles = file_utils.list_files(decompileDir, addFiles, igoreFileFullPaths)
    if len(addFiles) <= 0:
        return
    addCmd = '"%s" add "%s"'
    for f in addFiles:
        fname = f[len(decompileDir) + 1:]
        addCmd = addCmd + ' ' + fname

    addCmd = addCmd % (aapt, apkfile)
    currPath = os.getcwd()
    os.chdir(decompileDir)
    file_utils.execFormatCmd(addCmd, 'aaptAddFile')
    os.chdir(currPath)


def alignApk(apkfile, targetapkfile):
    """
        zip align the apk file
    """
    align = file_utils.getFullToolPath('zipalign')
    aligncmd = '"%s" -f 4 "%s" "%s"' % (align, apkfile, targetapkfile)
    ret = file_utils.execFormatCmd(aligncmd, 'alignApk')
    return ret


def getPackageName(decompileDir):
    """
        Get The package attrib of application node in AndroidManifest.xml
    """
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    package = root.attrib.get('package')
    return package


def renamePackageName(channel, decompileDir, newPackageName, isPublic = True):
    """
        Rename package name to the new name configed in the channel
    """
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    package = root.attrib.get('package')
    oldPackageName = package
    tempPackageName = newPackageName
    if not isPublic:
        newPackageName = oldPackageName + '.debug'
    if tempPackageName != None and len(tempPackageName) > 0:
        #判断填写的包名是否以‘.‘开头, 是的话新包名为在老包名后直接加上输入的包名，否则新包名为配置中填写的
        if tempPackageName[0:1] == '.':
            if not isPublic:
                newPackageName = oldPackageName + '.debug' + tempPackageName
            else:
                newPackageName = oldPackageName + tempPackageName
        else:
            newPackageName = tempPackageName
    if newPackageName == None or len(newPackageName) <= 0:
        newPackageName = oldPackageName
    log_utils.info('renamePackageName >>> the new package name is： %s', newPackageName)
    appNode = root.find('application')
    if appNode != None:
        activityLst = appNode.findall('activity')
        key = '{' + androidNS + '}name'
        if activityLst != None and len(activityLst) > 0:
            for aNode in activityLst:
                activityName = aNode.attrib[key]
                if activityName[0:1] == '.':
                    activityName = oldPackageName + activityName
                elif activityName.find('.') == -1:
                    activityName = oldPackageName + '.' + activityName
                aNode.attrib[key] = activityName

        serviceLst = appNode.findall('service')
        if serviceLst != None and len(serviceLst) > 0:
            for sNode in serviceLst:
                serviceName = sNode.attrib[key]
                if serviceName[0:1] == '.':
                    serviceName = oldPackageName + serviceName
                elif serviceName.find('.') == -1:
                    serviceName = oldPackageName + '.' + serviceName
                sNode.attrib[key] = serviceName

        receiverLst = appNode.findall('receiver')
        if receiverLst != None and len(receiverLst) > 0:
            for sNode in receiverLst:
                receiverName = sNode.attrib[key]
                if receiverName[0:1] == '.':
                    receiverName = oldPackageName + receiverName
                elif receiverName.find('.') == -1:
                    receiverName = oldPackageName + '.' + receiverName
                sNode.attrib[key] = receiverName

        providerLst = appNode.findall('provider')
        if providerLst != None and len(providerLst) > 0:
            for sNode in providerLst:
                providerName = sNode.attrib[key]
                if providerName[0:1] == '.':
                    providerName = oldPackageName + providerName
                elif providerName.find('.') == -1:
                    providerName = oldPackageName + '.' + providerName
                sNode.attrib[key] = providerName

    root.attrib['package'] = newPackageName
    tree.write(manifestFile, 'UTF-8')
    package = newPackageName
    return package


def copyResource(game, channel, packageName, sdkDir, decompileDir, operations, name, pluginInfo = None):
    """
        Copy sdk resources to the apk decompile dir
    
        Merge manifest.xml
        Merge all res xml if the xml already exists in target apk.
        copy all others resources
    """
    if operations != None:
        for child in operations:
            if child['type'] == 'mergeManifest':
                manifestFrom = file_utils.getFullPath(os.path.join(sdkDir, child['from']))
                #SDKManifest.xml
                manifestFromTemp = manifestFrom
                #AndoidManifest.xml
                manifestTo = file_utils.getFullPath(os.path.join(decompileDir, child['to']))
                if 'orientation' in game:
                    if game['orientation'] == 'portrait':
                        #SDKManifest_portrait.xml
                        manifestFrom = manifestFrom[:-4] + '_portrait.xml'
                    else:
                        #SDKManifest_landscape.xml
                        manifestFrom = manifestFrom[:-4] + '_landscape.xml'
                    if not os.path.exists(manifestFrom):
                        manifestFrom = manifestFromTemp
                log_utils.info('The sdk manifest file is %s', manifestFrom)
                bRet = mergeManifest(manifestTo, manifestFrom)
                if bRet:
                    log_utils.info('merge manifest file success.')
                else:
                    log_utils.error('merge manifest file failed.')
                    return 1
            elif child['type'] == 'copyRes':
                if child['from'] == None or child['to'] == None:
                    log_utils.error("the sdk config file error. 'copyRes' need 'from' and 'to'.sdk name: %s", name)
                    return 1
                copyFrom = file_utils.getFullPath(os.path.join(sdkDir, child['from']))
                copyTo = file_utils.getFullPath(os.path.join(decompileDir, child['to']))
                if child['to'] == 'lib':
                    copyLibs(game, copyFrom, copyTo)
                else:
                    copyResToApk(copyFrom, copyTo)
            elif child['type'] == 'script' and pluginInfo != None:
                if child['from'] == None:
                    log_utils.error("the sdk config file is error. 'script' need 'from' attrib to specify script.py")
                    return 1
                scriptName = child['from']
                log_utils.info('now to execute plugin script. name:%s', scriptName)
                doScript(channel, pluginInfo, decompileDir, packageName, sdkDir, scriptName)

    return 0


def copyChannelResources(game, channel, decompileDir):
    """
        Copy channel resources to decompile folder. for example icon resources, assets and so on.
    """
    resPath = 'config/games/' + game['appName'] + '/channels/' + channel['id']
    resPath = file_utils.getFullPath(resPath)
    if not os.path.exists(resPath):
        log_utils.warning('the channel %s special res path is not exists. %s', channel['id'], resPath)
        return 0
    targetResPath = file_utils.getFullPath(decompileDir)
    copyResToApk(resPath, targetResPath)
    log_utils.info('copy channel %s special res to apk success.', channel['name'])
    return 0


def copyAppResources(game, decompileDir):
    """
        Copy game res files to apk.
    """
    resPath = 'config/games/' + game['appName'] + '/res'
    resPath = file_utils.getFullPath(resPath)
    if not os.path.exists(resPath):
        log_utils.warning('the game %s has no extra res folder', game['appName'])
        return
    assetsPath = os.path.join(resPath, 'assets')
    libsPath = os.path.join(resPath, 'libs')
    resourcePath = os.path.join(resPath, 'res')
    targetAssetsPath = os.path.join(decompileDir, 'assets')
    targetLibsPath = os.path.join(decompileDir, 'libs')
    targetResourcePath = os.path.join(decompileDir, 'res')
    decompileDir = file_utils.getFullPath(decompileDir)
    copyResToApk(assetsPath, targetAssetsPath)
    copyResToApk(libsPath, targetLibsPath)
    copyResToApk(resourcePath, targetResourcePath)


def copyAppRootResources(game, decompileDir):
    """
        Copy game root files to apk. the files will be in the root path of apk
    """
    resPath = 'config/games/' + game['appName'] + '/root'
    resPath = file_utils.getFullPath(resPath)
    if not os.path.exists(resPath):
        log_utils.info('the game %s has no root folder', game['appName'])
        return
    targetResPath = file_utils.getFullPath(decompileDir)
    copyResToApk(resPath, targetResPath)


def mergeManifest(targetManifest, sdkManifest):
    """
        Merge sdk SdkManifest.xml to the apk AndroidManifest.xml
    """
    if not os.path.exists(targetManifest) or not os.path.exists(sdkManifest):
        log_utils.error('The manifest file is not exists.targetManifest: %s; sdkManifest: %s', targetManifest, sdkManifest)
        return False
    ET.register_namespace('android', androidNS)
    targetTree = ET.parse(targetManifest)
    targetRoot = targetTree.getroot()
    ET.register_namespace('android', androidNS)
    sdkTree = ET.parse(sdkManifest)
    sdkRoot = sdkTree.getroot()
    f = open(targetManifest)
    targetContent = f.read()
    f.close()
    permissionConfigNode = sdkRoot.find('permissionConfig')
    if permissionConfigNode != None and len(permissionConfigNode) > 0:
        for child in list(permissionConfigNode):
            key = '{' + androidNS + '}name'
            val = child.get(key)
            if val != None and len(val) > 0:
                attrIndex = targetContent.find(val)
                if -1 == attrIndex:
                    targetRoot.append(child)

    appConfigNode = sdkRoot.find('applicationConfig')
    appNode = targetRoot.find('application')
    if appConfigNode != None:
        proxyApplicationName = appConfigNode.get('proxyApplication')
        if proxyApplicationName != None and len(proxyApplicationName) > 0:
            metaNode = SubElement(appNode, 'meta-data')
            key = '{' + androidNS + '}name'
            val = '{' + androidNS + '}value'
            metaNode.set(key, 'RH_APPLICATION_PROXY_NAME')
            metaNode.set(val, proxyApplicationName)
        appKeyWord = appConfigNode.get('keyword')
        for child in list(appConfigNode):
            targetRoot.find('application').append(child)

    targetTree.write(targetManifest, 'UTF-8')
    return True


def copyResToApk(copyFrom, copyTo):
    """
        Copy two resource folders
    """
    if not os.path.exists(copyFrom):
        log_utils.error('the copyFrom %s is not exists.', copyFrom)
        return
    if not os.path.exists(copyTo):
        os.makedirs(copyTo)
    if os.path.isfile(copyFrom) and not mergeResXml(copyFrom, copyTo):
        file_utils.copyFile(copyFrom, copyTo)
        return
    for f in os.listdir(copyFrom):
        sourcefile = os.path.join(copyFrom, f)
        targetfile = os.path.join(copyTo, f)
        if os.path.isfile(sourcefile):
            if not os.path.exists(copyTo):
                os.makedirs(copyTo)
            if mergeResXml(sourcefile, targetfile):
                continue
            if not os.path.exists(targetfile) or os.path.getsize(targetfile) != os.path.getsize(sourcefile):
                destfilestream = open(targetfile, 'wb')
                sourcefilestream = open(sourcefile, 'rb')
                destfilestream.write(sourcefilestream.read())
                destfilestream.close()
                sourcefilestream.close()
        if os.path.isdir(sourcefile):
            copyResToApk(sourcefile, targetfile)


def mergeResXml(copyFrom, copyTo):
    """
        Merge all android res xml
    """
    if not os.path.exists(copyTo):
        return False
    aryXml = ['strings.xml',
     'styles.xml',
     'colors.xml',
     'dimens.xml',
     'ids.xml',
     'attrs.xml',
     'integers.xml',
     'arrays.xml',
     'bools.xml',
     'drawables.xml']
    basename = os.path.basename(copyFrom)
    if basename in aryXml:
        if config_utils.is_py_env_2():
            f = open(copyTo)
        else:
            f = open(copyTo, 'r', encoding='utf-8')
        targetContent = f.read()
        f.close()
        fromTree = ET.parse(copyFrom)
        fromRoot = fromTree.getroot()
        toTree = ET.parse(copyTo)
        toRoot = toTree.getroot()
        for node in list(fromRoot):
            val = node.get('name')
            if val != None and len(val) > 0:
                valMatched = '"' + val + '"'
                attrIndex = targetContent.find(valMatched)
                if -1 == attrIndex:
                    toRoot.append(node)
                else:
                    log_utils.warning('The node %s is already exists in %s', val, basename)

        toTree.write(copyTo, 'UTF-8')
        return True
    return False


def copySplashToUnityResFolder(workDir, channel, decompileDir):
    splashPath = file_utils.getSplashPath()
    resPath = workDir + '/sdk/' + channel['name'] + '/splash/' + channel['splash'] + '/%s/yinhu_splash.png'
    resTargetPath = decompileDir + '/assets/bin/Data/splash.png'
    paths = ['drawable',
     'drawable-hdpi',
     'drawable-ldpi',
     'drawable-mdpi',
     'drawable-xhdpi']
    bFound = False
    for path in paths:
        imgPath = resPath % path
        if os.path.exists(imgPath):
            resPath = imgPath
            bFound = True
            break

    if not bFound:
        log_utils.error('the yinhu_splash is not found.path:%s', resPath)
        return 1
    if not os.path.exists(resTargetPath):
        log_utils.error('the unity splash is not exists. path:%s', resTargetPath)
        return 1
    file_utils.copy_file(resPath, resTargetPath)
    return 0


def addSplashScreen(workDir, channel, decompileDir):
    """
        if the splash attrib is not zero ,then set the splash activity
        if the splash_copy_to_unity attrib is set, then copy the splash img to unity res fold ,replace the default splash.png.
    
    """
    if channel['splash'] == '0':
        return 0
    if channel['splash_copy_to_unity'] == '1':
        return copySplashToUnityResFolder(workDir, channel, decompileDir)
    splashPath = file_utils.getSplashPath()
    smaliPath = splashPath + '/smali'
    smaliTargetPath = decompileDir + '/smali'
    copyResToApk(smaliPath, smaliTargetPath)
    splashLayoutPath = splashPath + '/rh_splash.xml'
    splashTargetPath = decompileDir + '/res/layout/rh_splash.xml'
    file_utils.copy_file(splashLayoutPath, splashTargetPath)
    resPath = workDir + '/sdk/' + channel['sdk'] + '/splash/' + channel['splash']
    resTargetPath = decompileDir + '/res'
    copyResToApk(resPath, resTargetPath)
    activityName = removeStartActivity(decompileDir)
    appendSplashActivity(decompileDir, channel['splash'])
    splashActivityPath = smaliTargetPath + '/com/paojiao/rhsdk/SplashActivity.smali'
    f = open(splashActivityPath, 'r+')
    content = str(f.read())
    f.close()
    replaceTxt = '{RHSDK_Game_Activity}'
    idx = content.find(replaceTxt)
    if idx == -1:
        log_utils.error('modify splash file failed.the {RHSDK_Game_Activity} not found in SplashActivity.smali')
        return 1
    content = content[:idx] + activityName + content[idx + len(replaceTxt):]
    f2 = open(splashActivityPath, 'w')
    f2.write(content)
    f2.close()
    log_utils.info('modify splash file success.')
    return 0


def removeStartActivity(decompileDir):
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    applicationNode = root.find('application')
    if applicationNode is None:
        return
    activityNodeLst = applicationNode.findall('activity')
    if activityNodeLst is None:
        return
    activityName = ''
    for activityNode in activityNodeLst:
        bMain = False
        intentNodeLst = activityNode.findall('intent-filter')
        if intentNodeLst is None:
            break
        for intentNode in intentNodeLst:
            bFindAction = False
            bFindCategory = False
            actionNodeLst = intentNode.findall('action')
            if actionNodeLst is None:
                break
            for actionNode in actionNodeLst:
                if actionNode.attrib[key] == 'android.intent.action.MAIN':
                    bFindAction = True
                    break

            categoryNodeLst = intentNode.findall('category')
            if categoryNodeLst is None:
                break
            for categoryNode in categoryNodeLst:
                if categoryNode.attrib[key] == 'android.intent.category.LAUNCHER':
                    bFindCategory = True
                    break

            if bFindAction and bFindCategory:
                bMain = True
                intentNode.remove(actionNode)
                intentNode.remove(categoryNode)
                break

        if bMain:
            activityName = activityNode.attrib[key]
            break

    tree.write(manifestFile, 'UTF-8')
    return activityName


def appendSplashActivity(decompileDir, splashType):
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    key = '{' + androidNS + '}name'
    screenkey = '{' + androidNS + '}screenOrientation'
    theme = '{' + androidNS + '}theme'
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    applicationNode = root.find('application')
    if applicationNode is None:
        return
    splashNode = SubElement(applicationNode, 'activity')
    splashNode.set(key, 'com.paojiao.rhsdk.SplashActivity')
    splashNode.set(theme, '@android:style/Theme.Black.NoTitleBar.Fullscreen')
    if splashType[:1] == '1':
        splashNode.set(screenkey, 'landscape')
    else:
        splashNode.set(screenkey, 'portrait')
    intentNode = SubElement(splashNode, 'intent-filter')
    actionNode = SubElement(intentNode, 'action')
    actionNode.set(key, 'android.intent.action.MAIN')
    categoryNode = SubElement(intentNode, 'category')
    categoryNode.set(key, 'android.intent.category.LAUNCHER')
    tree.write(manifestFile, 'UTF-8')


def handleThirdPlugins(workDir, decompileDir, game, channel, packageName):
    pluginsFolder = file_utils.getFullPath('config/plugin')
    gamePluginFolder = file_utils.getFullPath('config/games/' + game['appName'] + '/plugin')
    plugins = channel.get('third-plugins')
    if plugins == None or len(plugins) <= 0:
        log_utils.info('the channel %s has no supported plugins.', channel['name'])
        return 0
    for plugin in plugins:
        pluginName = plugin['name']
        pluginSourceFolder = os.path.join(pluginsFolder, pluginName)
        if not os.path.exists(pluginSourceFolder):
            log_utils.warning('the plugin %s config folder is not exists', pluginName)
            continue
        pluginTargetFolder = workDir + '/plugins/' + pluginName
        file_utils.copy_files(pluginSourceFolder, pluginTargetFolder)
        gamePluginSourceFolder = os.path.join(gamePluginFolder, pluginName)
        if not os.path.exists(gamePluginSourceFolder):
            log_utils.warning('the plugin %s is not configed in the game %s', pluginName, game['appName'])
            continue
        file_utils.copy_files(gamePluginSourceFolder, pluginTargetFolder)
        if not os.path.exists(pluginSourceFolder + '/classes.dex'):
            jar2dex(pluginSourceFolder, pluginTargetFolder)

    smaliDir = os.path.join(decompileDir, 'smali')
    pluginNum = 0
    for plugin in plugins:
        pluginName = plugin['name']
        pluginFolder = workDir + '/plugins/' + pluginName
        if not os.path.exists(pluginFolder):
            log_utils.warning('the plugin %s temp folder is not exists', pluginName)
            continue
        pluginDexFile = os.path.join(pluginFolder, 'classes.dex')
        ret = dex2smali(pluginDexFile, smaliDir, 'baksmali.jar')
        if ret:
            return 1
        ret = copyResource(game, channel, packageName, pluginFolder, decompileDir, plugin['operations'], pluginName, plugin)
        if ret:
            return 1
        pluginNum += 1

    log_utils.info('Total plugin num:%s;success handle num:%s', str(len(plugins)), str(pluginNum))


def generateNewRFile(newPackageName, decompileDir):
    """
        Use all new resources to generate the new R.java, and compile it ,then copy it to the target smali dir
    """
    ret = checkValueResources(decompileDir)
    if ret:
        return 1
    decompileDir = file_utils.getFullPath(decompileDir)
    tempPath = os.path.dirname(decompileDir)
    tempPath = tempPath + '/temp'
    log_utils.debug('generate R:the temp path is %s', tempPath)
    if os.path.exists(tempPath):
        file_utils.del_file_folder(tempPath)
    if not os.path.exists(tempPath):
        os.makedirs(tempPath)
    resPath = os.path.join(decompileDir, 'res')
    targetResPath = os.path.join(tempPath, 'res')
    file_utils.copy_files(resPath, targetResPath)
    genPath = os.path.join(tempPath, 'gen')
    if not os.path.exists(genPath):
        os.makedirs(genPath)
    aaptPath = file_utils.getFullToolPath('aapt')
    androidPath = file_utils.getFullToolPath('android.jar')
    manifestPath = os.path.join(decompileDir, 'AndroidManifest.xml')
    cmd = '"%s" p -f -m -J "%s" -S "%s" -I "%s" -M "%s"' % (aaptPath,
     genPath,
     targetResPath,
     androidPath,
     manifestPath)
    ret = file_utils.execFormatCmd(cmd, 'generateNewRFile')
    if ret:
        return 1
    rPath = newPackageName.replace('.', '/')
    rPath = os.path.join(genPath, rPath)
    rPath = os.path.join(rPath, 'R.java')
    cmd = '"%sjavac" -source 1.7 -target 1.7 -encoding UTF-8 "%s"' % (file_utils.getJavaBinDir(), rPath)
    ret = file_utils.execFormatCmd(cmd, 'compileRFile')
    if ret:
        return 1
    targetDexPath = os.path.join(tempPath, 'classes.dex')
    if platform.system() == 'Windows':
        dexToolPath = file_utils.getFullToolPath('dx.bat')
        cmd = '"%s" --dex --output="%s" "%s"' % (dexToolPath, targetDexPath, genPath)
    else:
        dexToolPath = file_utils.getFullToolPath('/lib/dx.jar')
        cmd = file_utils.getJavaCMD() + ' -jar -Xmx512m -Xms512m "%s" --dex --output="%s" "%s"' % (dexToolPath, targetDexPath, genPath)
    ret = file_utils.execFormatCmd(cmd, 'jar2dex')
    if ret:
        return 1
    smaliPath = os.path.join(decompileDir, 'smali')
    ret = dex2smali(targetDexPath, smaliPath, 'baksmali.jar')
    return ret


def writeDevelopInfo(appID, channel, decompileDir):
    developConfigFile = os.path.join(decompileDir, 'assets')
    if not os.path.exists(developConfigFile):
        os.makedirs(developConfigFile)
    developConfigFile = os.path.join(developConfigFile, 'developer_config.properties')
    config_utils.writeDeveloperProperties(appID, channel, developConfigFile)


def writePluginInfo(channel, decompileDir):
    developConfigFile = os.path.join(decompileDir, 'assets')
    if not os.path.exists(developConfigFile):
        os.makedirs(developConfigFile)
    developConfigFile = os.path.join(developConfigFile, 'plugin_configs.xml')
    config_utils.writePluginConfigs(channel, developConfigFile)


def writeManifestMetaInfo(channel, decompileDir):
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    key = '{' + androidNS + '}name'
    val = '{' + androidNS + '}value'
    appNode = root.find('application')
    if appNode is None:
        return
    metaDataList = appNode.findall('meta-data')
    if metaDataList != None:
        for metaDataNode in metaDataList:
            keyName = metaDataNode.attrib[key]
            for child in channel['params']:
                if keyName == child['name'] and child['bWriteInManifest'] == '1':
                    log_utils.warning('the meta-data node %s repeated. remove it .', keyName)
                    appNode.remove(metaDataNode)

            if 'third-plugins' in channel and channel['third-plugins'] != None and len(channel['third-plugins']) > 0:
                for cPlugin in channel['third-plugins']:
                    if 'params' in cPlugin and cPlugin['params'] != None and len(cPlugin['params']) > 0:
                        for child in cPlugin['params']:
                            if keyName == child['name'] and child['bWriteInManifest'] == '1':
                                log_utils.warning('the meta-data node %s repeated. remove it .', keyName)
                                appNode.remove(metaDataNode)

    for child in channel['params']:
        if child['bWriteInManifest'] != None and child['bWriteInManifest'] == '1':
            metaNode = SubElement(appNode, 'meta-data')
            metaNode.set(key, child['name'])
            metaNode.set(val, child['value'])

    if 'third-plugins' in channel and channel['third-plugins'] != None and len(channel['third-plugins']) > 0:
        for cPlugin in channel['third-plugins']:
            if 'params' in cPlugin and cPlugin['params'] != None and len(cPlugin['params']) > 0:
                for child in cPlugin['params']:
                    if child['bWriteInManifest'] != None and child['bWriteInManifest'] == '1':
                        metaNode = SubElement(appNode, 'meta-data')
                        metaNode.set(key, child['name'])
                        metaNode.set(val, child['value'])

    tree.write(manifestFile, 'UTF-8')
    log_utils.info('The manifestFile meta-data write successfully')


def doScript(channel, pluginInfo, decompileDir, packageName, sdkTempDir, scriptName):
    if scriptName != 'script.py':
        log_utils.error('the script file name must be script.py')
        return 1
    sdkScript = os.path.join(sdkTempDir, scriptName)
    if not os.path.exists(sdkScript):
        return 0
    sys.path.append(sdkTempDir)
    import script
    ret = script.execute(channel, pluginInfo, decompileDir, packageName)
    del sys.modules['script']
    sys.path.remove(sdkTempDir)
    return ret


def doSDKScript(channel, decompileDir, packageName, sdkTempDir):
    sdkScript = os.path.join(sdkTempDir, 'sdk_script.py')
    if not os.path.exists(sdkScript):
        return 0
    sys.path.append(sdkTempDir)
    import sdk_script
    ret = sdk_script.execute(channel, decompileDir, packageName)
    del sys.modules['sdk_script']
    sys.path.remove(sdkTempDir)
    return ret


def doGamePostScript(game, channel, decompileDir, packageName):
    scriptDir = file_utils.getFullPath('config/games/' + game['appName'] + '/scripts')
    if not os.path.exists(scriptDir):
        log_utils.info('the game post script is not exists. if you have some specail logic, you can do it in config/games/[yourgame]/scripts/post_script.py')
        return 0
    sdkScript = os.path.join(scriptDir, 'post_script.py')
    if not os.path.exists(sdkScript):
        log_utils.info('the game post script is not exists. if you have some specail logic, you can do it in config/games/[yourgame]/scripts/post_script.py')
        return 0
    sys.path.append(scriptDir)
    import post_script
    log_utils.info('------------------now to execute post_script.py of game %s ', game['appName'])
    ret = post_script.execute(game, channel, decompileDir, packageName)
    del sys.modules['post_script']
    sys.path.remove(scriptDir)
    return ret

def checkValueResources(decompileDir):
    valXmls = ['strings.xml',
     'styles.xml',
     'colors.xml',
     'dimens.xml',
     'ids.xml',
     'attrs.xml',
     'integers.xml',
     'arrays.xml',
     'bools.xml',
     'drawables.xml',
     'public.xml']
    resDir = decompileDir + '/res/values'
    existsStrs = {}
    stringsXml = resDir + '/strings.xml'
    if os.path.exists(stringsXml):
        stringTree = ET.parse(stringsXml)
        root = stringTree.getroot()
        for node in list(root):
            stringItem = {}
            name = node.attrib.get('name')
            val = node.text
            stringItem['file'] = stringsXml
            stringItem['name'] = name
            stringItem['value'] = val
            existsStrs[name] = stringItem

    existsColors = {}
    colorsXml = resDir + 'colors.xml'
    if os.path.exists(colorsXml):
        colorTree = ET.parse(colorsXml)
        root = colorTree.getroot()
        for node in list(root):
            colorItem = {}
            name = node.attrib.get('name')
            val = node.text.lower()
            colorItem['file'] = colorsXml
            colorItem['name'] = name
            colorItem['value'] = val
            existsColors[name] = colorItem

    valueFiles = {}
    for filename in os.listdir(resDir):
        if filename in valXmls:
            continue
        srcFile = os.path.join(resDir, filename)
        if os.path.splitext(srcFile)[1] != '.xml':
            continue
        tree = ET.parse(srcFile)
        root = tree.getroot()
        if root.tag != 'resources':
            continue
        for node in list(root):
            dictRes = None
            if node.tag == 'string':
                dictRes = existsStrs
            elif node.tag == 'color':
                dictRes = existsColors
            else:
                continue
            name = node.attrib.get('name')
            val = node.text
            if name is None:
                continue
            resItem = dictRes.get(name)
            if resItem is not None:
                resVal = resItem.get('value')
                log_utils.warning('node %s duplicated!!! the val is %s;the newVal is %s', name, val, resVal)
                if val.lower() == resVal.lower():
                    root.remove(node)
                else:
                    root.remove(node)
            else:
                valItem = {}
                valItem['file'] = srcFile
                valItem['name'] = name
                valItem['value'] = val
                dictRes[name] = valItem

        valueFiles[srcFile] = tree

    for valFile in valueFiles.keys():
        valueFiles[valFile].write(valFile, 'UTF-8')
    return 0


def getAppIconName(decompileDir):
    """
        \xe4\xbb\x8eAndroidManifest.xml\xe4\xb8\xad\xe8\x8e\xb7\xe5\x8f\x96\xe6\xb8\xb8\xe6\x88\x8f\xe5\x9b\xbe\xe6\xa0\x87\xe7\x9a\x84\xe5\x90\x8d\xe7\xa7\xb0
    """
    manifestFile = decompileDir + '/AndroidManifest.xml'
    manifestFile = file_utils.getFullPath(manifestFile)
    ET.register_namespace('android', androidNS)
    tree = ET.parse(manifestFile)
    root = tree.getroot()
    applicationNode = root.find('application')
    if applicationNode is None:
        return 'ic_launcher'
    key = '{' + androidNS + '}icon'
    log_utils.warning('=>AndroidManifest key : %s', key)
    iconName = applicationNode.get(key)
    if iconName is None:
        name = 'ic_launcher'
        return name
    name = iconName[10:]
    log_utils.warning('--------------------------------------->AndroidManifest key name: %s', name)
    return name


def appendChannelIconMark(game, channel, decompileDir):
    """

    """
    log_utils.warning('appendChannelIconMark： the game is: %s', game)
    gameName = 'icon.png'
    #config/games/rhsdk/icon/icon.png
    gameIconPath = 'config/games/' + game['appName'] + '/icon/' + gameName
    gameIconSpecialName = 'icon_special.png'
    gameIconSpecialPath = 'config/games/' + game['appName'] + '/icon/' + gameIconSpecialName
    gameIconPath = file_utils.getFullPath(gameIconPath)
    gameIconSpecialPath = file_utils.getFullPath(gameIconSpecialPath)
    log_utils.warning('appendChannelIconMark：icon path is : %s', gameIconPath)
    log_utils.warning('appendChannelIconMark: Special_Icon path is : %s', gameIconSpecialPath)
    #游戏配置目录icon文件夹内是没有名为icon_special.png的图片。
    if not os.path.exists(gameIconSpecialPath):
        log_utils.warning('appendChannelIconMark: Special_Icon path is not exists!!!')
        if not os.path.exists(gameIconPath):
            log_utils.error('appendChannelIconMark:  the game %s icon is not exists: %s', game['appName'], gameIconPath)
            #icon下未配置任何图片，直接退出此方法。
            return 1
        #icon是否需要添加角标
        useMark = True
        #在游戏渠道配置文件内是否设置了节点icon,不设置则不添加角标。
        if 'icon' not in channel:
            log_utils.warning('appendChannelIconMark： the channel %s of game %s do not config icon in config.xml,no icon mark.', channel['name'], game['appName'])
            useMark = False
        log_utils.warning('appendChannelIconMark： is true or false : %s', useMark)
        rlImg = Image.open(gameIconPath)
        #获取角标图片路径
        if useMark:
            markType = channel['icon']
            markName = 'right-bottom'
            if markType == 'rb':
                markName = 'right-bottom'
            elif markType == 'rt':
                markName = 'right-top'
            elif markType == 'lt':
                markName = 'left-top'
            elif markType == 'lb':
                markName = 'left-bottom'
            markPath = 'config/sdk/' + channel['sdk'] + '/icon_marks/' + markName + '.png'
            try:
                print 'CHANNELSDK ICON_MARKS NOT EXISTS'
            except Exception as e:
                print e
                print 'CHANNELSDK Exception e'
                markPath = 'config/sdk/' + channel['sdk'] + '/icon_marks/' + markName + '.png'
                raise
            else:
                log_utils.warning('CHANNELSDK ==')
            finally:
                log_utils.warning('GameIconPath MarkPath is :  \n\t \t\t%s ', markPath)
                if not os.path.exists(markPath):
                    log_utils.warning('IconMarks Sorry -->>>>>Game IconMarks \n\t -- %s -- \n\t is not exists of sdk [ %s ]. No icon mark.', markPath, channel['sdk'])
                else:
                    markIcon = Image.open(markPath)
                    log_utils.warning('OK \t\t---- IconMarks is exit ----')
                    rlImg = image_utils.appendIconMark(rlImg, markIcon, (0, 0))

        ldpiSize = (36, 36)
        mdpiSize = (48, 48)
        hdpiSize = (72, 72)
        xhdpiSize = (96, 96)
        xxhdpiSize = (144, 144)
        xxxhdpiSize = (192, 192)
        ldpiIcon = rlImg.resize(ldpiSize, Image.ANTIALIAS)
        mdpiIcon = rlImg.resize(mdpiSize, Image.ANTIALIAS)
        hdpiIcon = rlImg.resize(hdpiSize, Image.ANTIALIAS)
        xhdpiIcon = rlImg.resize(xhdpiSize, Image.ANTIALIAS)
        xxhdpiIcon = rlImg.resize(xxhdpiSize, Image.ANTIALIAS)
        xxxhdpiIcon = rlImg.resize(xxxhdpiSize, Image.ANTIALIAS)
        ldpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-ldpi')
        mdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-mdpi')
        hdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-hdpi')
        xhdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-xhdpi')
        xxhdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-xxhdpi')
        xxxhdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-xxxhdpi')
        if not os.path.exists(ldpiPath):
            os.makedirs(ldpiPath)
        if not os.path.exists(mdpiPath):
            os.makedirs(mdpiPath)
        if not os.path.exists(hdpiPath):
            os.makedirs(hdpiPath)
        if not os.path.exists(xhdpiPath):
            os.makedirs(xhdpiPath)
        if not os.path.exists(xxhdpiPath):
            os.makedirs(xxhdpiPath)
        if not os.path.exists(xxxhdpiPath):
            os.makedirs(xxxhdpiPath)
        gameIconName = getAppIconName(decompileDir) + '.png'
        ldpiIcon.save(os.path.join(ldpiPath, gameIconName), 'PNG')
        mdpiIcon.save(os.path.join(mdpiPath, gameIconName), 'PNG')
        hdpiIcon.save(os.path.join(hdpiPath, gameIconName), 'PNG')
        xhdpiIcon.save(os.path.join(xhdpiPath, gameIconName), 'PNG')
        xxhdpiIcon.save(os.path.join(xxhdpiPath, gameIconName), 'PNG')
        xxxhdpiIcon.save(os.path.join(xxxhdpiPath, gameIconName), 'PNG')
    #游戏配置目录icon文件夹内是有名为icon_special.png的图片，使用该图片作为应用icon。
    else:
        log_utils.warning('appendChannelIconMark： Special_Icon path is exists!!! ')
        if not os.path.exists(gameIconSpecialPath):
            log_utils.error('appendChannelIconMark: Special the game %s icon is not exists:%s', game['appName'], gameIconSpecialPath)
            return 1
        useMark = True
        if 'icon' not in channel:
            log_utils.warning('GameIconPath Special the channel %s of game %s do not config icon in config.xml,no icon mark.', channel['name'], game['appName'])
            useMark = False
        log_utils.warning('appendChannelIconMark: Special useMark is True')
        rlImg = Image.open(gameIconSpecialPath)
        if useMark:
            markType = channel['icon']
            markName = 'right-bottom'
            if markType == 'rb':
                markName = 'right-bottom'
            elif markType == 'rt':
                markName = 'right-top'
            elif markType == 'lt':
                markName = 'left-top'
            elif markType == 'lb':
                markName = 'left-bottom'
            markPath = 'config/sdk/' + channel['sdk'] + '/icon_marks/' + markName + '.png'
            log_utils.warning('appendChannelIconMark: Special MarkPath is :%s ', markPath)
            if not os.path.exists(markPath):
                log_utils.warning('appendChannelIconMark: Game IconMarks  -- %s -- is not exists of sdk [ %s ]. No icon mark.', markPath, channel['sdk'])
            else:
                markIcon = Image.open(markPath)
                log_utils.warning('appendChannelIconMark: Special IconMarks is exit!!!')
                rlImg = image_utils.appendIconMark(rlImg, markIcon, (0, 0))
        #生成各种尺寸的app icon
        ldpiSize = (36, 36)
        mdpiSize = (48, 48)
        hdpiSize = (72, 72)
        xhdpiSize = (96, 96)
        xxhdpiSize = (144, 144)
        xxxhdpiSize = (192, 192)
        ldpiIcon = rlImg.resize(ldpiSize, Image.ANTIALIAS)
        mdpiIcon = rlImg.resize(mdpiSize, Image.ANTIALIAS)
        hdpiIcon = rlImg.resize(hdpiSize, Image.ANTIALIAS)
        xhdpiIcon = rlImg.resize(xhdpiSize, Image.ANTIALIAS)
        xxhdpiIcon = rlImg.resize(xxhdpiSize, Image.ANTIALIAS)
        xxxhdpiIcon = rlImg.resize(xxxhdpiSize, Image.ANTIALIAS)
        ldpiIconV4 = rlImg.resize(ldpiSize, Image.ANTIALIAS)
        mdpiIconV4 = rlImg.resize(mdpiSize, Image.ANTIALIAS)
        hdpiIconV4 = rlImg.resize(hdpiSize, Image.ANTIALIAS)
        xhdpiIconV4 = rlImg.resize(xhdpiSize, Image.ANTIALIAS)
        xxhdpiIconV4 = rlImg.resize(xxhdpiSize, Image.ANTIALIAS)
        xxxhdpiIconV4 = rlImg.resize(xxxhdpiSize, Image.ANTIALIAS)
        ldpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-ldpi')
        mdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-mdpi')
        hdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-hdpi')
        xhdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-xhdpi')
        xxhdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-xxhdpi')
        xxxhdpiPath = file_utils.getFullPath(decompileDir + '/res/drawable-xxxhdpi')
        ldpiPathV4 = file_utils.getFullPath(decompileDir + '/res/drawable-ldpi-v4')
        mdpiPathV4 = file_utils.getFullPath(decompileDir + '/res/drawable-mdpi-v4')
        hdpiPathV4 = file_utils.getFullPath(decompileDir + '/res/drawable-hdpi-v4')
        xhdpiPathV4 = file_utils.getFullPath(decompileDir + '/res/drawable-xhdpi-v4')
        xxhdpiPathV4 = file_utils.getFullPath(decompileDir + '/res/drawable-xxhdpi-v4')
        xxxhdpiPathV4 = file_utils.getFullPath(decompileDir + '/res/drawable-xxxhdpi-v4')
        if not os.path.exists(ldpiPath):
            os.makedirs(ldpiPath)
        if not os.path.exists(mdpiPath):
            os.makedirs(mdpiPath)
        if not os.path.exists(hdpiPath):
            os.makedirs(hdpiPath)
        if not os.path.exists(xhdpiPath):
            os.makedirs(xhdpiPath)
        if not os.path.exists(xxhdpiPath):
            os.makedirs(xxhdpiPath)
        if not os.path.exists(xxxhdpiPath):
            os.makedirs(xxxhdpiPath)
        iconPicNames = getAppIconName(decompileDir)
        #删除以下文件夹内指定名称的文件，以下操作是删除名字与application节点下icon指定值得图片 如：ic_launcher.png
        if os.path.exists(ldpiPathV4):
            file_search.printPats(1, ldpiPathV4, iconPicNames)
        if os.path.exists(mdpiPathV4):
            file_search.printPats(1, mdpiPathV4, iconPicNames)
        if os.path.exists(hdpiPathV4):
            file_search.printPats(1, hdpiPathV4, iconPicNames)
        if os.path.exists(xhdpiPathV4):
            file_search.printPats(1, xhdpiPathV4, iconPicNames)
        if os.path.exists(xxhdpiPathV4):
            file_search.printPats(1, xxhdpiPathV4, iconPicNames)
        if os.path.exists(xxxhdpiPathV4):
            file_search.printPats(1, xxxhdpiPathV4, iconPicNames)
        gameIconName = getAppIconName(decompileDir) + '.png'
        log_utils.warning('appendChannelIconMark： Special gameIconName: %s', gameIconName)
        #在以下每个文件夹内添加处理好的应用图标
        ldpiIcon.save(os.path.join(ldpiPath, gameIconName), 'PNG')
        mdpiIcon.save(os.path.join(mdpiPath, gameIconName), 'PNG')
        hdpiIcon.save(os.path.join(hdpiPath, gameIconName), 'PNG')
        xhdpiIcon.save(os.path.join(xhdpiPath, gameIconName), 'PNG')
        xxhdpiIcon.save(os.path.join(xxhdpiPath, gameIconName), 'PNG')
        xxxhdpiIcon.save(os.path.join(xxxhdpiPath, gameIconName), 'PNG')
    return 0


def splitDex(workDir, decompileDir):
    """
        如果函数上限超过限制，自动拆分smali，以便生成多个dex文件
    """
    #根据配置设置使用dex拆分
    local_config = config_utils.getLocalConfig()
    if 'split_dex' not in local_config :
        log_utils.info("The split_dex is not exists in local.properties. don't use split_dex.")
        return
    if not local_config['split_dex'] == '0':
        log_utils.info("The split_dex value is not '0', don't use split_dex.")
        return

    log_utils.info("now to check split dex ... ")

    smaliPath = decompileDir + "/smali"

    multidexFilePath = file_utils.getFullPath(smaliPath + "/android/support/multidex/MultiDex.smali")
    if not os.path.exists(multidexFilePath):
        #android-support-multidex.jar不存在，从local下面拷贝，并编译
        dexJar = file_utils.getFullPath('config/local/android-support-multidex.jar')
        if not os.path.exists(dexJar):
            log_utils.error("the method num expired of dex, but no android-support-multidex.jar in rh.apk or in local folder")
            return

        targetPath = file_utils.getFullPath(workDir + "/local")
        if not os.path.exists(targetPath):
            os.makedirs(targetPath)

        file_utils.copy_file(dexJar, targetPath+"/android-support-multidex.jar")

        jar2dex(targetPath, targetPath)
        smaliPath = file_utils.getFullPath(decompileDir + "/smali")
        ret = dex2smali(targetPath + '/classes.dex', smaliPath)



    allFiles = []
    allFiles = file_utils.list_files(decompileDir, allFiles, [])

    maxFuncNum = 65535
    currFucNum = 0
    totalFucNum = 0

    currDexIndex = 1

    allRefs = []

    #保证RHApplication等类在第一个classex.dex文件中
    for f in allFiles:
        f = f.replace("\\", "/")
        if "/com/paojiao/rhsdk" in f or "/android/support/multidex" in f:
            currFucNum = currFucNum + smali_utils.get_smali_method_count(f, allRefs)

    totalFucNum = currFucNum
    for f in allFiles:

        f = f.replace("\\", "/")
        if not f.endswith(".smali"):
            continue

        if "/com/paojiao/rhsdk" in f or "/android/support/multidex" in f:
            continue

        thisFucNum = smali_utils.get_smali_method_count(f, allRefs)
        totalFucNum = totalFucNum + thisFucNum

        if currFucNum + thisFucNum >= maxFuncNum:
            currFucNum = thisFucNum
            currDexIndex = currDexIndex + 1
            newDexPath = os.path.join(decompileDir, "smali_classes"+str(currDexIndex))
            os.makedirs(newDexPath)
        else:
            currFucNum = currFucNum + thisFucNum


        if currDexIndex > 1:
            targetPath = f[0:len(decompileDir)] + "/smali_classes"+str(currDexIndex) + f[len(smaliPath):]
            file_utils.copy_file(f, targetPath)
            file_utils.del_file_folder(f)


    log_utils.info("the total func num: "+str(totalFucNum))
    log_utils.info("split dex success. the classes.dex num: "+str(currDexIndex))


def isset(v):
    try:
        type(eval(v))
    except:
        return 0

    return 1