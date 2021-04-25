import re
from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
import requests
from determinecrawl import should_crawl, atags
from reports import get_reports, analyze_page, tokenize
from lxml import html

def scraper(url, resp)->list:
    if resp.status == 200:
        # no error status: return valid URLs
        links = extract_next_links(url, resp)
        get_reports()
        return links
    else:
        return []

def extract_next_links(url, resp):
    '''Finds linked webpages from a link.'''
    # the following code block is largely credited to the following documentation:
    # https://www.kite.com/python/answers/how-to-get-href-links-from-urllib-urlopen-in-python

    soup = BeautifulSoup(resp.raw_response.text, 'lxml')

    # check if there are too many atags compared to text (trap), or if there is no text
    if atags(url, soup):
        return []
    
    relative = urlparse(url)

    tokenize(url, soup)
    links = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        # getting rid of fragment
        href = urldefrag(href)[0]
        
        # make url relative path
        parsed = urlparse(href)
        if parsed.scheme == '' and parsed.netloc == '':
            href = urljoin(url, href)

        #print(href)
        
        # check if this page can/should be crawled if it is a valid url
        if is_valid(href) and should_crawl(href, parsed):
            # print('\nhecc yes\n')
            links.add(href)
            analyze_page(href)

    return list(links)

def is_valid(url):
    '''Return a boolean value to indicate whether or not the url is valid or not.
        As per assignment specs, only URLs under the school of ICS are valid.'''
    try:
        parsed = urlparse(url)

        if parsed.scheme not in ["http", "https"]:
            return False

        if not re.match(r".*\.(ics|cs|informatics|stat|today)\.uci\.edu$", parsed.netloc):
            return False

        if re.match(r".*\.today\.uci\.edu$", parsed.netloc) and not re.match(r".*\/department\/information_computer_sciences$", parsed.path):
            return False
        
        if re.match(r".*(pdf|img).*", parsed.path.lower()):
            return False
        
        if re.match(r"^replytocom=.*", parsed.query.lower()):
            return False

        return not re.match(    # if file extension is in the path
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf|ppsx|ppt"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise