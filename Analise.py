# coding: latin-1
import json
import re
import operator
from collections import Counter
from nltk.corpus import stopwords
from nltk import bigrams
import string
import time

from nltk.tokenize import word_tokenize

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

'''r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '''

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE | re.UNICODE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

punctuation = list(string.punctuation)
stop = stopwords.words('portuguese') + punctuation + ['rt', 'via', 'https', 'http']

'''with open('olimpiadas23.json', 'r') as f:
    line = f.readline() # read only the first tweet/line
    tweet = json.loads(line) # load it as Python dict
    print(json.dumps(tweet, indent=4)) # pretty-print'''

with open('/home/matheus/Documents/Estudo/MBCA/Monografia/Programa/dados/olimpiadasfullpt.json', 'r') as f:
    count_all = Counter()
    start_time = time.time()
    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_stop = [term for term in preprocess(tweet['text'], True) if term not in stop]
        # Update the counter
        count_all.update(terms_stop)
    # Print the first 5 most frequent words
    print("--- %s seconds ---" % (time.time() - start_time))

    word_freq = count_all.most_common(100)
    print(word_freq)
