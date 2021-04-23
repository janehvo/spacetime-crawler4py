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
from urllib.parse import urlparse
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
longest_page = ('', 0)  # determining this by word count
token_frequencies = defaultdict(int)
ics_subdomains = defaultdict(int)

def check_icssubdomain(url:str):
    parsed = urlparse(url)
    if re.match(r".*\.ics\.uci\.edu$", parsed.netloc):
        ics_subdomains[parsed.scheme + '://' + parsed.netloc] += 1
    return


def computeWordFrequencies(tokens: list):
    '''Counts the number of occurences of each token in a list of tokens.'''
    global most_common
    for t in tokens:
        tokenFrequency[t] += 1
    return
   

def tokenize(url, soup):
    global longest_page
    # initialize regex sequence for alphanumeric strings
    sequence = re.compile(r'^[a-zA-z0-9]*$')
    # initialize empty set to store unique tokens
    tokens = []

    for text in soup.get_text():
        # concantenate apostrophes, then strip puncuation from the text
        text = text.replace('\'', '')
        text = re.sub(r'[^\w\s]', ' ', text)
        # get individual words in the line
        for word in text.split():
            if re.match(sequence, word) and word not in stopwords and len(word) > 2:
                # any string with the same characters, no matter the case, are the considered the same
                tokens.append(word.lower())

    computeWordFrequencies(tokens)
    # check if this is the longest page
    page_length = len(tokens)
    if page_length > longest_page[1]:
        longest_page = (url, page_length)


def analyze_page(url:str):
    global unique_urls
    # unique pages
    unique_urls.add(url)
    # check if the it as a subdomain of .ics.uci.edu
    check_icssubdomain(url)
    # find all tokens in page
    tokenize(url)


def get_reports():
    '''Write scrape analystics to a file.'''
    file = open("reports.py", "w")

    # unique pages
    wstring = "[1] Number of unique pages found: " + str(len(unique_urls)) + ".\n"
    file.write(wstring)

    # longest page
    wstring = "\n[2] Longest page in terms of number of words: " + longest_page[0] + ", whose length is " + str(longest_page[1] + "\n")
    file.write(wstring)

    # 50 most common words. in descending order
    wstring = "\n[3] The 50 most common words:\n"
    count = 1
    file.write(wstring)
    for token in sorted(token_frequencies, key = lambda x: -token_frequencies[x]):
        file.write(str(count) + ". " + token + "-->" + token_frequencies[token] + "\n")
        count += 1
        if count == 51:
            break

    # number of ics.uci.edu subdomains, in alphabetical order
    wstring = "\n[4]Subdomains of ics.uci.edu that were found:\n"
    file.write(wstring)
    for subdomain in sorted(ics_subdomains.keys()):
        file.write(subdomain + ", " + ics_subdomains[subdomain] + "\n")
    