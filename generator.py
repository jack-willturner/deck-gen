import glob
import os
import xml.etree.ElementTree as ET
import argparse
import genanki
import re
from collections import Counter
from collections import Iterable
from tqdm import tqdm

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default='./xml', help='Where are the subtitles relative to me?')
parser.add_argument("-o", "--output", type=str, default='./decks', help='Where do you want me to save the decks I generate?')
args = parser.parse_args()

# anki defaults
model_id = 1237575582
deck_id  = 1250240356


my_model = genanki.Model(
  model_id,
  'Simple Model',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': '{{Question}}',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

my_deck = genanki.Deck(
    deck_id,
    'Marseilles'
)

episodes = []
num_episodes = 1

class Row:
    def __init__(self, begin, end, text):
        self.begin = begin
        self.end   = end
        self.text  = text

def transpose_xmltree(tree):
    rows = [] # use a list since we'll be traversing anyway
    for child in tree.iter():
        if 'begin' in child.attrib:
            begin = int(child.attrib['begin'][:-1])
            end   = int(child.attrib['end'][:-1])
            text  = child.text

            newRow = Row(begin, end, text)
            rows.append(newRow)
    return rows

def get_overlap(a, b):
    return max(0, min(a[1], b[1]) - max(a[0], b[0]))

# horrible range intersection code
def get_best_overlap(s_child, target_tree):
    s_range = range(s_child.begin, s_child.end)
    size_of_range = len(s_range)
    percentage_threshold = int(size_of_range * 0.8)

    # we're going to traverse the target tree and find the most overlapping subtitle
    best_overlap_node = None

    for t_child in target_tree:
        # get the time range for the node
        overlap = get_overlap((s_child.begin, s_child.end), (t_child.begin, t_child.end))
        if overlap > percentage_threshold:
            best_overlap = overlap
            best_overlap_node = t_child
            break

        if (t_child.begin > s_child.end):
            best_overlap_node = None
            break

    return best_overlap_node


def get_lines_from_episode(source, target):
    source_tree, target_tree = transpose_xmltree(ET.parse(source)), transpose_xmltree(ET.parse(target))
    s_lines, t_lines = [], []
    p = re.compile('[\[\]]')

    for s_child in source_tree:
        t_child = get_best_overlap(s_child, target_tree)
        if t_child is not None:
            s_lines.append(s_child.text)
            t_lines.append(t_child.text)

    return s_lines, t_lines


def filter_non_words(l):
    p = re.compile('[-\[\]:?.]') # it turns out i have no idea how to use regex's any more
    return list([w.lower() for w in l if p.search(w) is None])

os.chdir(args.input)
for ep_num in range(1, num_episodes+1):
    source = 'source_ep' + str(ep_num) + '.xml'
    target = 'target_ep' + str(ep_num) + '.xml'
    source_lines, target_lines = get_lines_from_episode(source, target)

    # for s,t in zip(source_lines, target_lines):
        if (s is not None) and (t is not None):
            note = genanki.Note(
                model=my_model,
                fields=[s, t]
            )
            my_deck.add_note(note)

os.chdir('../decks')
pack = genanki.Package(my_deck)
pack.write_to_file('marseilles_ep1.apkg')
