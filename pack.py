# 2017.01.16 18:56:25 �й���׼ʱ��
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
    parser = argparse.ArgumentParser(u'�����������ĳ����������')
    parser.add_argument('-r', '--release', help=u'���Ϊ��ʽ��������ʽ�����ڰ����������.debug', action='store_true', dest='release', default=False)
    parser.add_argument('-s', '--select', help=u'���û��Լ�ѡ����Ҫ��������������򽫻�������������', action='store_true', dest='selectable', default=False)
    parser.add_argument('-t', '--thread', help=u'ȫ�����ʱ�Ĵ���߳�����', action='store', dest='threadNum', type=int, default=1)
    parser.add_argument('-v', '--version', help=u'�鿴��ǰʹ�õ�YinHuSDK�汾', version='V2.3', action='version', default='V2.3')
    args = parser.parse_args()
    print args
    games.entry(args.release, args.selectable, args.threadNum, args.version)

# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2017.01.16 18:56:25 �й���׼ʱ��
