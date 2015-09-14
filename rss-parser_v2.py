#!/usr/bin/python
#-*- coding:utf-8 -*-


"""
    Keyword-based fileterind for RSS Parser
    Create by password123456
    edited by crattack
"""

import os, sys, time, re
import feedparser
import urllib, urllib2

# used korea language
reload(sys)
sys.setdefaultencoding('utf-8')
#


# RSS Config
sURLfile = './Monitor_url.txt'
sResultfile = './Recently_feed_log.txt'
sFullLogFile = './Feed_Full_log.txt'
#

# Feed Saved Limit Time
iLimitTime = 12 * 3600 * 1000
#

# Get Time Variable
iGetMStime = int(round(time.time() * 1000))
#

def isCheckSite(sSiteName):
    try:

        if os.path.exists(sResultfile):
            fpContent = open(sResultfile, 'r')
            for strLine in fpContent:
                if sSiteName in strLine:
                    return True

    except Exception, e:
        print (' ConnectSite Exception : ' + e + '\n')

    return False 

def isCheckNewIssue(sSiteName):
    try:
        if os.path.exists(sResultfile):
            strContent = open(sResultfile, 'r')
            for strLine in strContent:
                if sSiteName in strLine:
                    iTime = long(strLine.split('|', 1)[1])
                    if iGetMStime - iTime > iLimitTime:
                        return True

    except Exception, e:
        print (' ConnectSite Exception : ' + e + '\n')

    return False 

def ConnectSite(sURLAddr, sSiteName):
    pGetContent = []
    pExceptContent = []

    strKeyword = ['bind',
                  'critical',
                  'cve',
                  'openssl',
                  '원격',
                  '코드',
                  '실행',
                  'flash',
                  'player',
                  'tomcat',
                  'my',
                  'sql',
                  'apple-sa']
   
    sURLContent = feedparser.parse(sURLAddr)
    #print ('RSS Contents = %s\n' % sURLContent)
    
    for sURLtitle in sURLContent.entries:
        try:
            if not os.path.exists(sFullLogFile): fpFullLog = open(sFullLogFile, 'w')
            else: fpFullLog = open(sFullLogFile, 'a')

            fpFullLog.write(sSiteName + '  ' + sURLtitle.title + '\n ===> ' + sURLtitle.link + '\n')

        except Exception, e:
            print (' Full Log File Exception : ' + e + '\n')

        fpFullLog.close()

        
        for strKey in strKeyword:
            if strKey.upper() in sURLtitle.title.upper():
                # Test Code Log Write....    
                #print strKey
                #print sURLtitle.title
                ##########

                sSendMsg = sSiteName + '  ' + sURLtitle.title + '\n ===> ' + sURLtitle.link
                #print ('Site Link = %s\n' % sSendMsg)

                if isCheckNewIssue(sSiteName):
                    pExceptContent.append(sSiteName)
                        
                else:
                    pGetContent.append(sSiteName)
                    try:
                        if not os.path.exists(sResultfile): fpResult = open(sResultfile, 'w')
                        else: fpResult = open(sResultfile, 'a')

                        if not isCheckSite(sSiteName):
                            fpResult.write(sSiteName + sURLtitle.title + ' | ' + str(iGetMStime) + '\n')
                            print sSendMsg
                        else:
                            pass
                    except Exception, e:
                        print (' ConnectSite Exception : ' + e + '\n')
    return

def Get_Monitoring_URL():
    try:
        if os.path.exists(sURLfile):
            fpURL = open(sURLfile,'r')
            # file line read.
            for line in fpURL.read().split('\n'):
                sSiteName = line.split(',')[0]
                #print ('Site Name : %s\n' % sSiteName)

                sURLAddr = line.split(',')[-1]
                #print ('Site Address : %s\n' % sURLAddr)

                ConnectSite(sURLAddr, sSiteName)
            
        else:
            print ('[-] URL Text File not Found.\n[%s] Check please.\n' %
                    sURLfile)
            
        fpURL.close()
    except Exception, e:
        print (' Get Monitoring URL Exception : ' + e + '\n')
 

def main():
    Get_Monitoring_URL()

if __name__ == '__main__':
    main()

