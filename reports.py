# ======= Handle assignment output requirements here =======

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
longest_page = ('', 0)
token_frequencies = defaultdict(int)
ics_subdomains = defaultdict(int)


def token_frequencies(tokens: list):
    '''Counts the number of occurences of each token in a list of tokens.'''
    global token_frequencies
    for t in tokens:
        token_frequencies[t] += 1
   

def tokenize(url, soup):
    '''Find all tokens in a page and get word count.'''
    global longest_page
    global stopwords

    # initialize regex sequence for alphabetic strings (excluding numeric strings)
    sequence = re.compile(r'^[a-zA-Z]*$')

    tokens = []
    word_count = 0
    
    for text in soup.get_text().split():
        # up the word count
        word_count += 1
        # concantenate apostrophes, then strip puncuation from the text
        text = text.replace('\'', '')
        text = re.sub(r'[^\w\s]', ' ', text)
        if re.match(sequence, text) and text not in stopwords and len(text) > 2:
            # any string with the same characters, no matter the case, are the considered the same
            tokens.append(text.lower())

    token_frequencies(tokens)
    # check if this is the longest page
    if word_count > longest_page[1]:
        longest_page = (url, words)


def check_icssubdomain(url:str):
    '''Check if url is a subdomain of ics.uci.edu.'''
    parsed = urlparse(url)
    if re.match(r".*\.ics\.uci\.edu$", parsed.netloc):
        ics_subdomains[parsed.scheme + '://' + parsed.netloc] += 1


def analyze_page(url:str):
    global unique_urls
    # unique pages
    unique_urls.add(url)
    # check if the it as a subdomain of .ics.uci.edu
    check_icssubdomain(url)


def get_reports():
    '''Write scrape analystics to a file.'''
    # optional print to console
    print('\nunique_urls: ', str(len(unique_urls)), '\n')
    
    file = open("reports.txt", "w")

    # unique pages
    wstring = "[1] Number of unique pages found: " + str(len(unique_urls)) + ".\n"
    file.write(wstring)

    # longest page
    wstring = "\n[2] Longest page in terms of number of words: " + longest_page[0] + ", whose length is " + str(longest_page[1]) + "\n"
    file.write(wstring)

    # 50 most common words, in descending order
    wstring = "\n[3] The 50 most common words:\n"
    count = 1
    file.write(wstring)
    for token in sorted(token_frequencies, key = lambda x: -token_frequencies[x]):
        file.write(str(count) + ". " + token + " --> " + str(token_frequencies[token]) + "\n")
        count += 1
        if count == 51:
            break

    # number of ics.uci.edu subdomains, in alphabetical order
    wstring = "\n[4] Subdomains of ics.uci.edu that were found:\n"
    file.write(wstring)
    for subdomain in sorted(ics_subdomains.keys()):
        file.write(subdomain + ", " + str(ics_subdomains[subdomain]) + "\n")
