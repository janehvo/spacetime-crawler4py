# ======= Handle robots.txt and crawler traps ========
import requests
from urllib import robotparser
from collections import defaultdict
import re
from bs4 import BeautifulSoup

# robots that have been read already
robots_read = dict()

# TO DO: implement duplicate detection


def atags(url, soup)->bool:
    '''Pages with a large atag to text count is considered a trap. Return True if trap.'''
    try:
        atag_count = len(soup.find_all('a'))
        text_count = len(soup.get_text().split())

        # if this page has no textual content, count it as a trap and skip scraping it
        if text_count == 0:
            return True

        # if atag_count == text_count, that means the text is only from links
        # links can only account for 30% of the text (this tolerance may increase/decrease)
        return True if atag_count/text_count > .3 else False
    except ZeroDivisionError:
        # this means that the page has text only
        return False


# code extracted from urllib.robotparser documentation: 
# https://docs.python.org/3/library/urllib.robotparser.html
def check_robots(parsed)->bool:
    '''Check robots.txt. Return True if this agent is allowed to crawl, False otherwise.'''
    global robots_read
    robots_read[parsed.netloc] = False
    try:
        url = 'http://' + parsed.netloc + '/robots.txt'
        sitemap = requests.get(url)
        if sitemap.status_code != 200:
            return False
        rp = robotparser.RobotFileParser(url)
        rp.read()
        if rp.can_fetch('*', url):
            robots_read[parsed.netloc] = True
        return True
            
    except:
        # requests.get('http://' + parsed.netloc + '/robots.txt') throw and exception if no robots.txt is found
        return False


# crawler traps were identified with the references to:
# https://support.archive-it.org/hc/en-us/articles/208332943-Identify-and-avoid-crawler-traps-
def check_trap(url, parsed)->bool:
    '''Check if wehpage contain any crawler traps.
    Return True if it is not a trap, False if it is'''
    # check for long URLS
    if len(url) > 200:
        return False
    # check if there is a calendar, and avoid it
    if re.match(r"^.*calendar.*$", parsed.path.lower()):
        return False
    # archives are also a trap
    if re.match(r"^archive.*", parsed.path.lower()):
        return False
    # check repeating directories:
    if re.match(r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", parsed.path.lower()):
        return False
    # check extra directories
    if re.match(r"^.*(/misc|/sites|/all|/themes|/modules|/profiles|/css|/field|/node|/theme){3}.*$", parsed.path.lower()):
        return False
    return True


def should_crawl(url, parsed):
    ''' Determine whether a page should be crawled, whether it is a trap or because robots.txt'''
    global robots_read
    # if the robot has never been read
    if parsed.netloc not in robots_read:
        return check_robots(parsed) and check_trap(url, parsed)
    else:
        # if the robot has been read, check if site page is crawlable before checking for traps
        return robots_read[parsed.netloc] and check_trap(url, parsed)
