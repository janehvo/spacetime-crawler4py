# ======= Handle assignment output requirements here =======

# 1. How many unique pages did you find? Uniqueness for the purposes of this assignment is ONLY established by the URL, 
#    but discarding the fragment part. So, for example, http://www.ics.uci.edu#aaa and http://www.ics.uci.edu#bbb are the same URL. 
#    Even if you implement additional methods for textual similarity detection, please keep considering the above definition of unique pages 
#    for the purposes of counting the unique pages in this assignment.

# 2. What is the longest page in terms of the number of words? (HTML markup doesn’t count as words)

# 3. What are the 50 most common words in the entire set of pages crawled under these domains? 
#    (Ignore English stop words, which can be found, for example, here (Links to an external site.)) 
#    Submit the list of common words ordered by frequency.

# 4. How many subdomains did you find in the ics.uci.edu domain? Submit the list of subdomains ordered alphabetically and 
#    the number of unique pages detected in each subdomain. The content of this list should be lines containing URL, number, for example:
#    http://vision.ics.uci.edu, 10 (not the actual number here)

import requests
from urllib import urlparse
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
import re
from collections import defaultdict

# stopwords from https://www.ranks.nl/stopwords
stopwords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at", 
             "be", "because", "been", "before", "being", "below", "between", "both", "but", "by",
             "can't", "cannot", "could", "couldn't", "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
             "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't", "have", "haven't", "having",
             "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's",
             "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's", "its", "itself",
             "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not",
             "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own",
             "same", "shan't", "she", "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
             "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these",
             "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too",
             "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were", "weren't", "what",
             "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
             "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
             "yourself", "yourselves"]

unique_urls = set()
longest_page = ('', 0)
most_common = dict()
ics_subdomains = defaultdict(int)

def check_icssubdomain(url:str):
    parsed = urlparse(url)
    if re.match(r".*\.ics\.uci\.edu$", parsed.netloc):
        ics_subdomains[parsed.scheme + '://' + parsed.netloc] += 1
    return


def analyze_page(url:str):
    # unique pages
    unique_urls.add(url)
    # check if the it as a subdomain of .ics.uci.edu
    check_icssubdomain(url)
    # check page length


    return


def get_reports(links:list):
    return
    