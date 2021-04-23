import re
from urllib.parse import urlparse, urldefrag, urljoin
from bs4 import BeautifulSoup
import requests
from determinecrawl import should_crawl
from reports import get_reports, analyze_page, tokenize

def scraper(url, resp)->list:
    ''' NEED TO DEVELOP '''
    if 200 <= resp.status < 400:
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
    relative = urlparse(url)

    soup = BeautifulSoup(resp.raw_response.text, 'html.parser')

    # check if there are too many atags compared to text (trap)
    if atags(url, soup):
        return []

    tokenize(url, soup)
    links = set()
    for link in soup.find_all('a'):
        href = link.get('href')
        href = urldefrag(href)[0]

        # check if it is a relative path and if so, fill in the missing parts
        parsed = urlparse(href)
        if parsed.scheme == '' and parsed.netloc == '':
            parsed._replace(scheme=relative.scheme)
            parsed._replace(netloc=relative.netloc)
        else if parsed.scheme != '' and parsed.netloc == '':
            parsed._replace(netloc=relative.netloc)
        else if parsed.scheme == '' and parsed.netloc != '':
            parsed._replace(scheme=relative.scheme)

        href = parsed.geturl()
        
        # check if this page can/should be crawled if it is a valid url
        if is_valid(href) and should_crawl(href, parsed):
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

        return not re.match(    # if file extension is in the path
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):

    except TypeError:
        print ("TypeError for ", parsed)
        raise