# 2017.01.16 18:56:25 中国标准时间
#Embedded file name: pack.py
import games
import main
import main_thread
import sys
import http_utils
import argparse
import stat
import file_search
import log_utils
if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('gbk')
    parser = argparse.ArgumentParser(u'\u94f6\u72d0\u6280\u672f\u5927\u5927\u7684\u8d85\u7ea7\u6253\u5305\u5de5\u5177')
    parser.add_argument('-r', '--release', help=u'\u6807\u8bb0\u4e3a\u6b63\u5f0f\u5305\uff0c\u975e\u6b63\u5f0f\u5305\u4f1a\u5728\u5305\u540d\u540e\u9762\u52a0\u4e0a.debug', action='store_true', dest='release', default=False)
    parser.add_argument('-s', '--select', help=u'\u8ba9\u7528\u6237\u81ea\u5df1\u9009\u62e9\u9700\u8981\u6253\u5305\u7684\u6e20\u9053\u3002\u5426\u5219\u5c06\u4f1a\u6253\u51fa\u6240\u6709\u6e20\u9053\u5305', action='store_true', dest='selectable', default=False)
    parser.add_argument('-t', '--thread', help=u'\u5168\u90e8\u6253\u5305\u65f6\u7684\u6253\u5305\u7ebf\u7a0b\u6570\u91cf', action='store', dest='threadNum', type=int, default=1)
    parser.add_argument('-v', '--version', help=u'\u67e5\u770b\u5f53\u524d\u4f7f\u7528\u7684YinHuSDK\u7248\u672c', version='V2.3', action='version', default='V2.3')
    args = parser.parse_args()
    print args
    games.entry(args.release, args.selectable, args.threadNum, args.version)

# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.01.16 18:56:25 中国标准时间
