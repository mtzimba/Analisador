#!/usr/bin/python
# coding: latin-1
import json
import string

from nltk.corpus import stopwords
from nltk.tokenize import TweetTokenizer
from collections import Counter


def _str_to_unicode(text, encoding=None, errors='strict'):
    if encoding is None:
        encoding = 'latin-1'
    if isinstance(text, bytes):
        return text.decode(encoding, errors)
    return text

tt = TweetTokenizer()

punctuation = list(string.punctuation)
stop = stopwords.words('portuguese') + punctuation + ['rt', 'via', 'https', 'http','...']


listaHashtag = []
fo = open("olimpiadastesteprocessado.txt", "wb")
with open('olimpiadasteste.json', 'r') as f:
    for line in f:
        tweet = json.loads(line)
        if tweet['lang'] == 'pt':
            text = tweet['text'].lower()
            tokens = tt.tokenize(text)
            linhaProcessada = ""
            for toks in tokens:
                if toks.startswith('#'):
                    listaHashtag.append(toks)
                    print(toks)
                elif toks not in stop and \
                        not toks.startswith('https') and \
                        not toks.startswith('http') and \
                        not toks.startswith('@') and \
                        not toks.startswith('#'):
                    linhaProcessada += toks + " "
                    print(toks)
            fo.write(linhaProcessada.encode('utf-8') + "\n")
            print('----------------------------------------------------')
fo.close()

count_hashtag = Counter()
count_hashtag.update(listaHashtag)
word_freq = count_hashtag.most_common(100)
print(word_freq)