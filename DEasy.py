#!/usr/bin/python
'''
Created on Dec 30, 2013

@author: sai
'''

import requests
import os
from HTMLParser import HTMLParser
import sys
import pynotify


class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        '''
        This method overrides HTMLParser's corresponding method.
        we set a flag to know that our desired tag is reached 
        and data should be appended.
        '''
        if tag == 'div':
            for each_attr in attrs:
                if each_attr[0] == "class" and each_attr[1] == "ds-list":
                    #print "in start tag of div "
                    self.flag = True
                    self.data = ''

    def handle_endtag(self, tag):
        '''
        it is called when the parser encounters the end tag 
        for the html text. Checks the flag and proceeds accordingly.
        '''
        if self.flag == True:
            if tag == "div":
                #print "div is closed"
                raise Exception("End of parsing")

    def handle_data(self, data):
        '''
        It is called when ever the parse encounters a data
        member.
        '''
        if self.flag == True:
            #print data
            self.data = self.data + data






def main():
    CurString = os.popen("xsel").read()
    #print CurString
    if CurString == '':
        return
    http_proxy = os.environ['http_proxy']
    https_proxy = os.environ['https_proxy']
    proxy_info = {'http': http_proxy, 'https':https_proxy}
    #print proxy_info
    #CurString = "hi"
    res = requests.get("http://www.thefreedictionary.com/"+CurString, proxies=proxy_info)
    count = 1
    while res.status_code != 200 and count < 3 :
        res = requests.get("http://www.thefreedictionary.com/"+CurString, proxies=proxy_info)
        count = count + 1
    
    parser = MyHTMLParser()
    parser.flag = False
    parser.data = ''
    if res.status_code == 200:
        try:
            parser.feed(res.text)
        except:
            #parser.close()
            print "parsing completed"
        #parser.close()
        #print res.text
        if not pynotify.init("icon-summary-body"):
            sys.exit(1)
        #print parser.data
        n = pynotify.Notification(CurString,
                                      parser.data,
                                      "notification-message-im")
        n.show()
    else:
        print res.status_code


if __name__ == "__main__":
    main()
