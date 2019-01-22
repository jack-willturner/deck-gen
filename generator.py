import glob
import os
import xml.etree.ElementTree as ET
import argparse
from googletrans import Translator
from collections import Counter

directory = '.'
translator = Translator()

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", type=str, default=directory)
parser.add_argument("-o", "--output", type=str, default=directory)
args = parser.parse_args()

episodes = []

def get_lines_from_episode(xml_file):
    ep_tree = ET.parse(xml_file)
    ep_root = ep_tree.getroot()
    words = []

    for child in ep_tree.iter():
        if child.text:
            words.append(child.text)
    #ep_list = ET.fromstringlist(xml_file)
    return words

os.chdir(args.input)
for file in glob.glob("*.xml"):
    lines = get_lines_from_episode(file)
    words = [w for line in lines for w in line.split()]

    word_freqs = Counter(words)

    translations = translator.translate(words)
    print(translations)
    episodes.append(words)

for k, w in translations.items():
    print(k, w)
