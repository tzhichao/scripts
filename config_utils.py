# -*- coding:utf-8 -*-
import sys
import os
import os.path
import file_utils
import log_utils
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import SubElement
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import ElementTree

def getLocalConfig():
    configFile = file_utils.getFullPath('config/local/local.properties')
    if not os.path.exists(configFile):
        print 'local.properties is not exists. %s ' % configFile
        return None
    cf = open(configFile, 'r')
    lines = cf.readlines()
    cf.close()
    config = {}
    for line in lines:
        line = line.strip()
        dup = line.split('=')
        config[dup[0]] = dup[1]

    return config


def get_py_version():
    version = sys.version_info
    major = version.major
    minor = version.minor
    micro = version.micro
    currVersion = str(major) + '.' + str(minor) + '.' + str(micro)
    return currVersion


def is_py_env_2():
    version = sys.version_info
    major = version.major
    return major == 2


def getAllGames():
    """
        get all games
    """
    configFile = file_utils.getFullPath('config/games/games.xml')
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error('==> can not parse games.xml.path:%s', configFile)
        return

    gamesNode = root.find('games')
    if gamesNode == None:
        return
    games = gamesNode.findall('game')
    if games == None or len(games) <= 0:
        return
    lstGames = []
    for cNode in games:
        game = {}
        params = cNode.findall('param')
        if params != None and len(params) > 0:
            for cParam in params:
                key = cParam.get('name')
                val = cParam.get('value')
                game[key] = val

        lstGames.append(game)

    return lstGames


def getTestKeyStore():
    keystore = {}
    keystore['keystore'] = 'config/keystore/paojiao/pj_yh_key'
    keystore['password'] = 'k2faV3pp2AF43'
    keystore['aliaskey'] = 'paojiao'
    keystore['aliaspwd'] = 'g5s04kdx235d'
    return keystore


def getKeystore(appName, channelId):
    lstKeystores = getAllKeystores(appName)
    if lstKeystores != None and len(lstKeystores) > 0:
        for keystore in lstKeystores:
            if keystore['channelId'] == channelId:
                return keystore

    return getDefaultKeystore(appName)


def getDefaultKeystore(appName):
    fileName = 'config/games/' + appName + '/keystore.xml'
    configFile = file_utils.getFullPath(fileName)
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error('-------\xe3\x80\x8bcan not parse keystore.xml.path:%s', configFile)
        return None

    params = root.find('default').findall('param')
    channel = {}
    for cParam in params:
        key = cParam.get('name')
        val = cParam.get('value')
        channel[key] = val

    return channel


def getAllKeystores(appName):
    fileName = 'config/games/' + appName + '/keystore.xml'
    configFile = file_utils.getFullPath(fileName)
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error('can not parse keystore.xml.path:%s', configFile)
        return None

    channels = root.find('keystores').findall('channel')
    lstKeystores = []
    for cNode in channels:
        channel = {}
        params = cNode.findall('param')
        for cParam in params:
            key = cParam.get('name')
            val = cParam.get('value')
            channel[key] = val

        lstKeystores.append(channel)

    return lstKeystores


def getAppID():
    configFile = file_utils.getFullPath('config/config.xml')
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error('getAppID => can not parse config.xml.path:%s', configFile)
        return

    gameNode = root.find('game')
    if gameNode == None:
        return
    appID = gameNode.get('appID')
    return appID


def getAppKey():
    configFile = file_utils.getFullPath('config/config.xml')
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error('getAppKey => can not parse config.xml.path:%s', configFile)
        return

    gameNode = root.find('game')
    if gameNode == None:
        return
    appID = gameNode.get('appKey')
    return appID


def getAllChannels(appName, isPublic):
    fileName = 'config/games/' + appName + '/config.xml'
    configFile = file_utils.getFullPath(fileName)
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except Exception as e:
        log_utils.error('getAllChannels => can not parse config.xml.path:%s', configFile)
        return

    lstGPlugins = []
    globalPluginsNode = root.find('global-plugins')
    if globalPluginsNode is not None:
        globalPlugins = globalPluginsNode.findall('plugin')
        if globalPlugins is not None and len(globalPlugins) > 0:
            for pluginNode in globalPlugins:
                plugin = {}
                plugin['name'] = pluginNode.get('name')
                plugin['desc'] = pluginNode.get('desc')
                loadThirdPluginUserConfig(appName, plugin, plugin['name'])
                lstGPlugins.append(plugin)

    channels = root.find('channels').findall('channel')
    lstChannels = []
    for cNode in channels:
        channel = {}
        params = cNode.findall('param')
        for cParam in params:
            key = cParam.get('name')
            val = cParam.get('value')
            channel[key] = val

        sdkVersionNode = cNode.find('sdk-version')
        if sdkVersionNode != None and len(sdkVersionNode) > 0:
            versionCodeNode = sdkVersionNode.find('versionCode')
            versionNameNode = sdkVersionNode.find('versionName')
            if versionCodeNode != None and versionNameNode != None:
                channel['sdkLogicVersionCode'] = versionCodeNode.text
                channel['sdkLogicVersionName'] = versionNameNode.text
        sdkParams = cNode.find('sdk-params')
        tblSDKParams = {}
        if sdkParams != None:
            sdkParamNodes = sdkParams.findall('param')
            if sdkParamNodes != None and len(sdkParamNodes) > 0:
                for cParam in sdkParamNodes:
                    key = cParam.get('name')
                    val = cParam.get('value')
                    tblSDKParams[key] = val

        channel['sdkParams'] = tblSDKParams
        ret = loadChannelUserConfig(appName, channel)
        if ret:
            lstPlugins = lstGPlugins
            pluginsNode = cNode.find('plugins')
            if pluginsNode != None:
                pluginNodeLst = pluginsNode.findall('plugin')
                if pluginNodeLst != None and len(pluginNodeLst) > 0:
                    for cPlugin in pluginNodeLst:
                        plugin = {}
                        plugin['name'] = cPlugin.get('name')
                        exists = False
                        for p in lstPlugins:
                            if p['name'] == plugin['name']:
                                exists = True
                                break

                        if not exists:
                            plugin['desc'] = cPlugin.get('desc')
                            loadThirdPluginUserConfig(appName, plugin, plugin['name'])
                            lstPlugins.append(plugin)

                    channel['third-plugins'] = lstPlugins
            lstChannels.append(channel)

    return lstChannels


def loadThirdPluginUserConfig(appName, plugin, pluginName):
    configFile = file_utils.getFullPath('config/games/' + appName + '/plugin/' + pluginName + '/config.xml')
    if not os.path.exists(configFile):
        log_utils.error('------->>the plugin %s config.xml file is not exists.path:%s', pluginName, configFile)
        return 0
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except:
        log_utils.error('can not parse config.xml.path:%s', configFile)
        return 0

    configNode = root
    subpluginNodes = configNode.find('subplugins')
    if subpluginNodes != None and len(subpluginNodes) > 0:
        plugin['subplugins'] = []
        for subNode in subpluginNodes:
            subplugin = {}
            subplugin['name'] = subNode.get('name')
            subplugin['desc'] = subNode.get('desc')
            subplugin['CHANNELNAMES'] = subNode.get('CHANNELNAMES')
            subParamNodes = subNode.findall('param')
            subplugin['params'] = []
            if subParamNodes != None and len(subParamNodes) > 0:
                for subParamNode in subParamNodes:
                    param = {}
                    param['name'] = subParamNode.get('name')
                    param['value'] = subParamNode.get('value')
                    param['required'] = subParamNode.get('required')
                    param['showName'] = subParamNode.get('showName')
                    param['bWriteInManifest'] = subParamNode.get('bWriteInManifest')
                    param['bWriteInClient'] = subParamNode.get('bWriteInClient')
                    subplugin['params'].append(param)

            plugin['subplugins'].append(subplugin)

    paramNodes = configNode.find('params')
    plugin['params'] = []
    if paramNodes != None and len(paramNodes) > 0:
        for paramNode in paramNodes:
            param = {}
            param['name'] = paramNode.get('name')
            param['value'] = paramNode.get('value')
            param['required'] = paramNode.get('required')
            param['showName'] = paramNode.get('showName')
            param['bWriteInManifest'] = paramNode.get('bWriteInManifest')
            param['bWriteInClient'] = paramNode.get('bWriteInClient')
            plugin['params'].append(param)

    operationNodes = configNode.find('operations')
    plugin['operations'] = []
    if operationNodes != None and len(operationNodes) > 0:
        for opNode in operationNodes:
            op = {}
            op['type'] = opNode.get('type')
            op['from'] = opNode.get('from')
            op['to'] = opNode.get('to')
            plugin['operations'].append(op)

    pluginNodes = configNode.find('plugins')
    if pluginNodes != None and len(pluginNodes) > 0:
        plugin['plugins'] = []
        for pNode in pluginNodes:
            p = {}
            p['name'] = pNode.get('name')
            p['type'] = pNode.get('type')
            plugin['plugins'].append(p)

    return 1


def loadChannelUserConfig(appName, channel):
    configFile = file_utils.getFullPath('config/sdk/' + channel['sdk'] + '/config.xml')
    if not os.path.exists(configFile):
        log_utils.error('the config.xml is not exists of sdk %s.path:%s', channel['name'], configFile)
        return 0
    try:
        tree = ET.parse(configFile)
        root = tree.getroot()
    except:
        log_utils.error(' == can not parse == config.xml.path:%s', configFile)
        return 0

    configNode = root
    paramNodes = configNode.find('params')
    channel['params'] = []
    if paramNodes != None and len(paramNodes) > 0:
        for paramNode in paramNodes:
            param = {}
            param['name'] = paramNode.get('name')
            param['required'] = paramNode.get('required')
            if param['required'] == '1':
                key = param['name']
                if key in channel['sdkParams'] and channel['sdkParams'][key] != None:
                    param['value'] = channel['sdkParams'][key]
                else:
                    log_utils.error("the sdk %s 'sdkParam's is not all configed in the config.xml.path:%s", channel['name'], configFile)
                    return 0
            else:
                param['value'] = paramNode.get('value')
            param['showName'] = paramNode.get('showName')
            param['bWriteInManifest'] = paramNode.get('bWriteInManifest')
            param['bWriteInClient'] = paramNode.get('bWriteInClient')
            channel['params'].append(param)

    operationNodes = configNode.find('operations')
    channel['operations'] = []
    if operationNodes != None and len(operationNodes) > 0:
        for opNode in operationNodes:
            op = {}
            op['type'] = opNode.get('type')
            op['from'] = opNode.get('from')
            op['to'] = opNode.get('to')
            channel['operations'].append(op)

    pluginNodes = configNode.find('plugins')
    if pluginNodes != None and len(pluginNodes) > 0:
        channel['plugins'] = []
        for pNode in pluginNodes:
            p = {}
            p['name'] = pNode.get('name')
            p['type'] = pNode.get('type')
            channel['plugins'].append(p)

    versionNode = configNode.find('version')
    if versionNode != None and len(versionNode) > 0:
        versionCodeNode = versionNode.find('versionCode')
        versionNameNode = versionNode.find('versionName')
        if versionCodeNode != None and versionNameNode != None:
            channel['sdkVersionCode'] = versionCodeNode.text
            channel['sdkVersionName'] = versionNameNode.text
    return 1


def writeDeveloperProperties(appID, channel, targetFilePath):
    targetFilePath = file_utils.getFullPath(targetFilePath)
    proStr = ''
    if channel['params'] != None and len(channel['params']) > 0:
        for param in channel['params']:
            if param['bWriteInClient'] == '1':
                proStr = proStr + param['name'] + '=' + param['value'] + '\n'

    if 'sdkLogicVersionCode' in channel:
        proStr = proStr + 'SDK_VERSION_CODE=' + channel['sdkLogicVersionCode'] + '\n'
    proStr = proStr + 'ChannelGameId=' + channel['id'] + '\n'
    proStr = proStr + 'GameId=' + appID + '\n'
    #获取本地配置地址
    local_config = getLocalConfig()
    if 'sdk_config' in local_config:
        proStr = proStr + 'sdk_config=' + local_config['sdk_config'] + '\n'
    if 'verify_token' in local_config:
        proStr = proStr + 'verify_token=' + local_config['verify_token'] + '\n'

    plugins = channel.get('third-plugins')
    if plugins != None and len(plugins) > 0:
        for plugin in plugins:
            if 'params' in plugin and plugin['params'] != None and len(plugin['params']) > 0:
                for param in plugin['params']:
                    if param['bWriteInClient'] == '1':
                        proStr = proStr + param['name'] + '=' + param['value'] + '\n'

    log_utils.debug('The develop info is %s :\n', proStr)
    targetFile = open(targetFilePath, 'wb')
    proStr = proStr.encode('UTF-8')
    targetFile.write(proStr)
    targetFile.close()


def writePluginConfigs(channel, targetFilePath):
    targetTree = None
    targetRoot = None
    pluginNodes = None
    targetTree = ElementTree()
    targetRoot = Element('plugins')
    targetTree._setroot(targetRoot)
    if 'plugins' in channel:
        for plugin in channel['plugins']:
            typeTag = 'plugin'
            typeName = plugin['name']
            typeVal = plugin['type']
            pluginNode = SubElement(targetRoot, typeTag)
            pluginNode.set('name', typeName)
            pluginNode.set('type', typeVal)

    thirdPlugins = channel.get('third-plugins')
    if thirdPlugins != None and len(thirdPlugins) > 0:
        for cPlugin in thirdPlugins:
            if 'plugins' in cPlugin and cPlugin['plugins'] != None and len(cPlugin['plugins']) > 0:
                for plugin in cPlugin['plugins']:
                    typeTag = 'plugin'
                    typeName = plugin['name']
                    typeVal = plugin['type']
                    pluginNode = SubElement(targetRoot, typeTag)
                    pluginNode.set('name', typeName)
                    pluginNode.set('type', typeVal)

    targetTree.write(targetFilePath, 'UTF-8')