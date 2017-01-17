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
            print u'\u5bc6\u7801:', name
        elif tag == 'neighbor':
            name = attributes['name']
            direction = attributes['direction']
        elif tag == 'company':
            name = attributes['name']
            direction = attributes['direction']

    def endElement(self, tag):
        if self.CurrentData == 'times':
            print u'\u7b49\u5f85\u65f6\u95f4:', self.times
        elif self.CurrentData == 'year':
            print u'\u5e74\u4efd:', self.year
        elif self.CurrentData == 'neighbor':
            print u'\u90bb\u5c45:', self.neighbor
        elif self.CurrentData == 'company':
            print u'\u516c\u53f8:', self.company
        elif self.CurrentData == 'versionCode':
            print u'\u5f53\u524d\u4f7f\u7528\u7248\u672c:', self.versionCode
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