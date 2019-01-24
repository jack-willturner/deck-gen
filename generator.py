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
num_episodes = 1

def get_lines_from_episode(source, target):
    source_tree, target_tree = ET.parse(source), ET.parse(target)
    s_lines, t_lines = [], []
    p = re.compile('[\[\]]')
    for s_child, t_child in zip(source_tree.iter(), target_tree.iter()):
        if s_child.text and t_child.text:
            if (p.search(s_child.text) is None):
                s_lines.append(s_child.text)
                t_lines.append(t_child.text)

    return s_lines, t_lines

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
for ep_num in range(1, num_episodes+1):
    source = 'source_ep' + str(ep_num) + '.xml'
    target = 'target_ep' + str(ep_num) + '.xml'
    source_lines, target_lines = get_lines_from_episode(source, target)

    for s,t in zip(source_lines, target_lines):
        print(s, "\t\t\t : ", t)



    #words = filter_non_words(list(flatten([w for line in lines for w in line.split()])))
    #translations = []

    #word_freqs = Counter(words)
    #episodes.append(words)
