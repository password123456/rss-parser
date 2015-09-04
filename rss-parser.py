#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
 Keyword-based filtering for RSS Feed Parser
 created by password123456
"""

import os,sys,time,re
import feedparser
import urllib,urllib2
import codecs

reload(sys)
sys.setdefaultencoding('utf-8')

# RSS Feed URL
_FEED_URL_FILE = './feed_url.txt'
_FEEDS_DB = './feeds.db'

# Feed Store 5days
_LIMIT = 12 * 3600 * 1000

_CURRENT_TIME_MILLISEC = lambda: int(round(time.time() * 1000))
_CURRENT_TIMESTAMP = _CURRENT_TIME_MILLISEC()

def post_is_in_db(_FEED_TITLE):
    try:
        mode = 'r' if os.path.exists(_FEEDS_DB) else open(_FEEDS_DB, 'w')
        with open(_FEEDS_DB, mode) as database:
            for line in database:
                if _FEED_TITLE in line:
                    return True
        return False
    except:
        pass


def post_is_in_db_with_old_timestamp(_FEED_TITLE):
    try:
        mode = 'r' if os.path.exists(_FEEDS_DB) else open(_FEEDS_DB, 'w')
        with open(_FEEDS_DB, mode) as database:
            for line in database:
                if _FEED_TITLE in line:
                    _TS_AS_STRING = line.split('|', 1)[1]
                    TS = long(_TS_AS_STRING)
                    if _CURRENT_TIMESTAMP - TS > _LIMIT:
                        return True
        return False
    except:
        pass

def do_load_feed_url():
    try:
        if os.path.exists(_FEED_URL_FILE):
            f = open(_FEED_URL_FILE, 'r')
            for n,line in enumerate(f.read().split('\n')):
                _FEED_NAME = line.split(',')[0]
                _URL = line.split(',')[-1]
                #print _URL
                do_feed(_URL,_FEED_NAME)
            f.close()
        else:
            print('[-] RSS Feed file not found.! check %s' % _FEED_URL_FILE)
    except Exception, e:
        print e

def do_feed(_URL,_FEED_NAME):
    _GET_FEED = []
    _SKIP_FEED = []

    # You can apply which want to receive Feeds based on simple Regex. 
    _FEED_KEYWORD = ur"(?i)(\bCritical\b|\bCVE\b|\bopenssl\b|\b원격\s*코드\s*실행\b|\bFlash\s*Player\b|\bTomcat\b|\bbind\b|\bMy\s*sql\b|\bAPPLE-SA\b)"
    _FEED_REGEX = re.compile(_FEED_KEYWORD, flags=re.IGNORECASE)

    feed = feedparser.parse(_URL)

    for post in feed.entries:
        _FEED_TITLE = post.title
        _KEYWORD_MATCH = re.findall(_FEED_REGEX, _FEED_TITLE)

        if _KEYWORD_MATCH:
            _FEED_TITLE_LINK = _FEED_NAME + ' ' + post.title + '\n ==> ' + post.link

            if post_is_in_db_with_old_timestamp(_FEED_TITLE):
                _SKIP_FEED.append(_FEED_TITLE)
            else:
                _GET_FEED.append(_FEED_TITLE)

                try:
                    mode = 'a' if os.path.exists(_FEEDS_DB) else open(_FEEDS_DB, 'w')
                    with open(_FEEDS_DB, mode) as f:
                        for _FEED_TITLE in _GET_FEED:
                            if not post_is_in_db(_FEED_TITLE):
                                
                                f.write(_FEED_TITLE + " | " + str(_CURRENT_TIMESTAMP) + "\n")
                                print _FEED_TITLE_LINK
                                ## do your stuff here
                                ## Like Email / SMS Forwaring
                finally:
                    f.close()

def main():
    do_load_feed_url()

if __name__ == '__main__':
    main()
