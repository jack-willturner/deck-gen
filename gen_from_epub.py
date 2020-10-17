import nltk
import argparse
import numpy as np

from bs4 import BeautifulSoup
from nltk.tokenize import RegexpTokenizer

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--output", type=str, default='./decks', help='Where do you want me to save the decks I generate?')
parser.add_argument("--start_chapter", type=str, default=2, type=int, help='Which chapter should I start from?')
parser.add_argument("--end_chapter", type=str, default=48, type=int, help='Which chapter should I finish at?')

## unzipped epub location
BOOKNAME = lambda x : f"books/book_chap_{x}.htm"

args = parser.parse_args()

def tf(t, d):
    '''
    Fetch the term frequency of term t in document d

    Parameters
    ----------
    t : str
        The word to look up
    d : dict
        The term frequency dictionary for one document
    '''
    return d[t]

def idf(t, D):
    '''
    Fetch the inverse document frequency of term t in the set of documents D

    Parameters
    ----------
    t : str
        The word to look up
    D : list
        A list of frequency dictionaries, one for each document
    '''
    num_docs = len(D)
    num_docs_with_t = len([d for d in D if d.get(t) is not None])
    return np.log(num_docs / num_docs_with_t)

## compile the frequency tables for all documents
docs = []
for i in range(args.start_chapter,args.end_chapter):
    j = '{:03d}'.format(i)

    fname = BOOKNAME(j)
    with open(fname,'r') as html_doc:
        chap = BeautifulSoup(html_doc, 'html.parser')

    try:
        chap_text = " ".join([p.string.lower() for p in chap.find_all(class_='MsoNormal')])
    except:
        try:
            chap_text = " ".join([p.text.lower() for p in chap.find_all(class_='calibre11')])
        except:
            print(f"error in chapter {j}")
            continue

    total_terms = len(chap_text)

    tokenizer = RegexpTokenizer(r'\w+')
    toks = tokenizer.tokenize(chap_text)
    freq = nltk.FreqDist(toks)
    tf_t = {k:f/total_terms for (k,f) in freq.items()} # TF(t)
    docs.append(tf_t)

## for each document, calculate TF-IDF and return indicative words
for i in range(args.start_chapter,args.end_chapter):
    doc = docs[i]
    tf_idf = {}

    for term in doc:
        tf_idf[term] = tf(term, doc) * idf(term, docs)

    most_important = sorted(tf_idf.items(), key=lambda x: x[1], reverse=True)
