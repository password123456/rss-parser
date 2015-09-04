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
sResultfile = './Extrator_feed.txt'
#

# Feed Saved Limit Time
iLimitTime = 12 * 3600 * 1000
#

# Get Time Variable
iGetMStime = int(round(time.time() * 1000))
#

def isCheckSite(sSiteName):
    try:
        mode = 'r' if os.path.exists(sResultfile) else open(sResultfile, 'w')
        with open(sResultfile, mode) as fpContent:
            for strLine in fpContent:
                if sSiteName in strLine:
                    return True

        return False            
    except:
        pass

def isCheckNewIssue(sSiteName):
    try:
        mode = 'r' if os.path.exists(sResultfile) else open(sResultfile, 'w')
        with open(sResultfile, mode) as strContent:
            for strLine in strContent:
                iTime = long(strLine.split('|', 1)[1])
                if iGetMStime - iTime > iLimitTime:
                    return True
        return False                       

    except:
        pass

def ConnectSite(sURLAddr, sSiteName):
    pGetContent = []
    pExceptContent = []
    
    sURLContent = feedparser.parse(sURLAddr)
    #print ('RSS Contents = %s\n' % sURLContent)

    for sRecvContent in sURLContent.entries:
        sSiteLink = sSiteName + '  ' + sRecvContent.title + '\n ===> ' + sRecvContent.link
        #print ('Site Link = %s\n' % sSiteLink)

        if isCheckNewIssue(sSiteName):
            pExceptContent.append(sSiteName)
        else:
            pGetContent.append(sSiteName)

            try:
                mode = 'a' if os.path.exists(sResultfile) else open(sResultfile, 'w')
                with open(sResultfile, mode) as fpResult:
                     for sSiteName in pGetContent:
                        if not isCheckSite(sSiteName):
                            fpResult.write(sRecvContent.title + ' | ' + str(iGetMStime) + '\n')                   
                            print sSiteLink
                            
            except Exception, e:
                print (' ConnectSite Exception : ' + e + '\n')

def Get_Monitoring_URL():
    try:
        if os.path.exists(sURLfile):
            fpURL = open(sURLfile,'r')
            # file line read.
            for n, line in enumerate(fpURL.read().split('\n')):
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
        print e


def main():
    Get_Monitoring_URL()

if __name__ == '__main__':
    main()

