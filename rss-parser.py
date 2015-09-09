#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
 Keyword-based filtering for RSS Feed Parser
 created by password123456
"""

import os
import sys
import time
import re
import feedparser
import urllib,urllib2

reload(sys)
sys.setdefaultencoding('utf-8')

# RSS Feed URL
sFEED_URL_FILE = './feed_url.txt'
sFEEDS_DB = './feeds.db'

# Feed Store 5days
iLIMIT = 12 * 3600 * 1000

iCURRENT_TIME_MILLISEC = lambda: int(round(time.time() * 1000))
iCURRENT_TIMESTAMP = iCURRENT_TIME_MILLISEC()

def post_is_in_db(sFEED_TITLE):
    try:
        if os.path.exists(sFEEDS_DB):
            mode = 'a'
        else:
            mode = 'w'
        with open(sFEEDS_DB, mode) as database:
            for line in database:
                if sFEED_TITLE in line:
                    return True
        return False
    except:
        pass

def post_is_in_db_with_old_timestamp(sFEED_TITLE):
    try:
        if os.path.exists(sFEEDS_DB):
            mode = 'a'
        else:
            mode = 'w'
        with open(sFEEDS_DB, mode) as database:
            for line in database:
                if sFEED_TITLE in line:
                    _TS_AS_STRING = line.split('|', 1)[1]
                    TS = long(_TS_AS_STRING)
                    if iCURRENT_TIMESTAMP - TS > iLIMIT:
                        return True
        return False
    except:
        pass

def do_load_feed_url():
    try:
        if os.path.exists(sFEED_URL_FILE):
            f = open(sFEED_URL_FILE, 'r')
            for n,line in enumerate(f.read().split('\n')):
                _FEED_NAME = line.split(',')[0]
                _URL = line.split(',')[-1]
                #print _URL
                do_feed(_URL,_FEED_NAME)
            f.close()
        else:
            print('[-] RSS Feed file not found.! check %s' % sFEED_URL_FILE)
    except Exception, e:
        print e

def do_feed(_URL,_FEED_NAME):
    pGET_FEED = []
    pSKIP_FEED = []

    # You can apply which want to receive Feeds based on simple Regex.
    _FEED_KEYWORD = ur"(?i)(\bCritical\b|\bCVE\b|\bopenssl\b|\b원격\s*코드\s*실행\b \
    	                   |\bFlash\s*Player\b|\bTomcat\b|\bbind\b|\bMy\s*sql\b|\bAPPLE-SA\b)"

    _FEED_REGEX = re.compile(_FEED_KEYWORD, flags=re.IGNORECASE)

    feed = feedparser.parse(_URL)
    for post in feed.entries:
        sFEED_TITLE = post.title
        _KEYWORD_MATCH = re.findall(_FEED_REGEX, sFEED_TITLE)
        if _KEYWORD_MATCH:
            sFEED_TITLE_LINK = _FEED_NAME + ' ' + post.title + '\n ==> ' + post.link
            if post_is_in_db_with_old_timestamp(sFEED_TITLE):
                pSKIP_FEED.append(sFEED_TITLE)
            else:
                pGET_FEED.append(sFEED_TITLE)
                try:
                    if os.path.exists(sFEEDS_DB):
                        mode = 'a'
                    else:
                        mode = 'w'
                    with open(sFEEDS_DB, mode) as f:
                        for sFEED_TITLE in pGET_FEED:
                            if not post_is_in_db(sFEED_TITLE):
                                f.write(sFEED_TITLE + " | " + str(iCURRENT_TIMESTAMP) + "\n")
                                print sFEED_TITLE_LINK
                                ## do your stuff here
                                ## Like Email / SMS Forwaring
                finally:
                    f.close()
        else:
            pass


def main():
    do_load_feed_url()

if __name__ == '__main__':
    main()
