# -*- coding: utf-8 -*-
import games
import sys
import argparse

if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('gbk')
    parser = argparse.ArgumentParser(u'打包工具')
    parser.add_argument('-r', '--release', help=u'标记为正式包，非正式包会在包名后面加上.debug', action='store_true', dest='release', default=False)
    parser.add_argument('-s', '--select', help=u'让用户自己选择需要打包的渠道。否则将会打出所有渠道包', action='store_true', dest='selectable', default=False)
    parser.add_argument('-t', '--thread', help=u'全部打包时的打包线程数量', action='store', dest='threadNum', type=int, default=1)
    parser.add_argument('-v', '--version', help=u'查看当前使用的RHSDK版本', version='V1.0', action='version', default='V1.0')
    args = parser.parse_args()
    print args
    games.entry(args.release, args.selectable, args.threadNum, args.version)

