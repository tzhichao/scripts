# -*- coding:utf-8 -*-
import sys
import os
import os.path
import file_utils
import log_utils
import xml.sax
import sys

class CountryHandler(xml.sax.ContentHandler):

    def __init__(self):
        self.CurrentData = ''
        self.times = ''
        self.year = ''
        self.neighbor = ''
        self.neighborDirection = ''
        self.company = ''
        self.companyDirection = ''
        self.versionCode = ''

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == 'command':
            print '*****Command*****'
            name = attributes['name']
            print u'密码:', name
        elif tag == 'neighbor':
            name = attributes['name']
            direction = attributes['direction']
        elif tag == 'company':
            name = attributes['name']
            direction = attributes['direction']

    def endElement(self, tag):
        if self.CurrentData == 'times':
            print u'等待时间:', self.times
        elif self.CurrentData == 'year':
            print u'年份:', self.year
        elif self.CurrentData == 'neighbor':
            print u'邻居:', self.neighbor
        elif self.CurrentData == 'company':
            print u'公司:', self.company
        elif self.CurrentData == 'versionCode':
            print u'当前使用版本:', self.versionCode
        self.CurrentData = ''
        return '1'

    def characters(self, content):
        if self.CurrentData == 'times':
            self.times = content
        elif self.CurrentData == 'year':
            self.year = content
        elif self.CurrentData == 'company':
            self.company = content
        elif self.CurrentData == 'versionCode':
            self.versionCode = content
        elif self.CurrentData == 'neighbor':
            self.neighbor = content

    def getNNNN(self):
        return self.times


def getTimes(XMLPath):
    reload(sys)
    sys.setdefaultencoding('utf8')
    parser = xml.sax.make_parser()
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    Handler = CountryHandler()
    parser.setContentHandler(Handler)
    parser.parse(XMLPath + 'Company_Time.xml')
    return Handler.getNNNN()


if __name__ == '__main__':
    te = getTimes('../')
    print te