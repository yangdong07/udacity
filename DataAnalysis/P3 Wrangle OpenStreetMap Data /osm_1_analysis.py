# -*- coding: utf-8 -*-

import re
import xml.etree.cElementTree as ET

from pprint import pprint
from collections import defaultdict, Counter

# OSM_FILE = 'chengdu_china.osm'
OSM_FILE = 'shanghai_china.sample.osm'



def iter_elements(osm_file):
    with open(osm_file, 'r') as f:
        for event, element in ET.iterparse(f, events=("end",)):
            yield element


# 1. 有多少种标签？每种标签多少个？
# 2. 每种标签有哪些属性？ 统计一下
# 3. 标签与标签之间的关系

def count_tags(osm_file):
    tags = Counter()
    tag_attribs = defaultdict(Counter)    # tag:attribs:count
    tag_relations = defaultdict(set)
    for element in iter_elements(osm_file):
        tags[element.tag] += 1
        attribs = ','.join(sorted(element.attrib.keys()))
        tag_attribs[element.tag][attribs] += 1
        for child in element:
            tag_relations[element.tag].add(child.tag)
    pprint(dict(tags))
    pprint(dict(tag_attribs))
    pprint(tag_relations)


#
# def analysis_tag_attrib(osm_file):
#     names = set()
#     suffix_pattern = re.compile(u'(路|[\d一二三四五六七八九十]+号|街)$')
#     suffix = Counter()
#     keys = Counter()
#     highways = Counter()
#     for element in iter_elements(osm_file):
#         for child in element:
#             if child.tag == 'tag':
#                 key, value = child.attrib['k'], child.attrib['v']
#                 keys[key] += 1
#                 if key == 'highway':
#                     highways[value] += 1
#                 if key.startswith('addr') or key.startswith('official_name'):
#                     m = suffix_pattern.search(value)
#                     if m:
#                         suffix[m.group()] += 1
#                     else:
#                         suffix[value[-1]] += 1
#                     # print value
#                     # if value.endswith(u'速'):
#                     # if suffix_pattern.search(value):
#                     #     good_names.add(value)
#                     # else:
#                     #     bad_names.add(value)
#                 # elif key.startswith('addr'):
#                 #     print value
#     # pprint(keys)
#     for k, v in keys.most_common(100):
#         print k, v
#     # pretty_print(good_names, 'good_names')
#     # pretty_print(bad_names, 'bad_names', 100)
#


def pretty_print(iterable, description='', num=10):
    print description, len(iterable)
    for item in list(iterable)[:num]:
        print item


if __name__ == '__main__':
    count_tags(OSM_FILE)
