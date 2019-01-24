import glob
import os
import xml.etree.ElementTree as ET
import argparse
import re
from collections import Counter
from collections import Iterable
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default='./xml', help='Where are the subtitles relative to me?')
parser.add_argument("-o", "--output", type=str, default='./decks', help='Where do you want me to save the decks I generate?')
args = parser.parse_args()

episodes = []

def get_lines_from_episode(xml_file):
    ep_tree = ET.parse(xml_file)
    ep_root = ep_tree.getroot()
    words = []

    for child in ep_tree.iter():
        if child.text:
            words.append(child.text)

    return words

# with thanks to stackoverflow
def flatten(l):
    for el in l:
        if isinstance(el, Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

def filter_non_words(l):
    p = re.compile('[-\[\]:?.]') # it turns out i have no idea how to use regex's any more
    return list([w.lower() for w in l if p.search(w) is None])

os.chdir(args.input)
for file in glob.glob("*.xml"):
    lines = get_lines_from_episode(file)
    words = filter_non_words(list(flatten([w for line in lines for w in line.split()])))
    translations = []

    word_freqs = Counter(words)
    episodes.append(words)

print(translations)
