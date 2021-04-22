# ======= Handle robots.txt ========
import requests
from urllib import robotparser
from collections import defaultdict
import re

# robots that have been read already
robots_read = dict()

def check_robots(url, parsed)->bool:
    '''Check robots.txt. Return True if this agent is allowed to crawl, False otherwise.'''
    global robots_read
    robots_read[parsed.netloc] = False
    try:
        sitemap = requests.get('http://' + parsed.netloc + '/robots.txt')
        if sitemap.status_code != 200:
            return False
        parsedrobo = robotparser.RobotFileParser(sitemap)
        parsedrobo.read()
        if parsedrobo.can_fetch('*', sitemap):
            robots_read[parsed.netloc] = True
        return robots_read[parsed.netloc]
            
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
    if re.match(r"^.*calendaar.*$", parsed.path.lower()):
        return False
    if 'date' in parsed.params or 'year' in parsed.params.lower():
        return False
    # check repeating directories:
    if re.match(r"^.*?(/.+?/).*?\1.*$|^.*?/(.+?/)\2.*$", parsed.path):
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
        return check_robots(url, parsed) and check_trap(url, parsed)
    else:
        # if the robot has been read, check if site page is crawlable before checking for traps
        return check_trap(url, parsed) if robots_read[parsed.netloc] else False
