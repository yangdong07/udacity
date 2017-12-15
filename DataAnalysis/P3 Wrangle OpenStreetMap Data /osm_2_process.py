# -*- coding: utf-8 -*-

import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json


# OSM_FILE = 'chengdu_china.osm'
OSM_FILE = 'shanghai_china.osm'


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


CREATED = ["version", "changeset", "timestamp", "user", "uid"]


def _clean_tags(tags):
    data = {}
    name = tags.pop('name', None)
    names = set()
    address = dict()
    official_names = set()
    for k in tags.keys():
        if k.startswith('name:'):
            names.add(tags.pop(k))
        elif k.startswith('addr:'):
            address[k[5:]] = tags.pop(k)
        elif k.startswith('official_name:'):
            official_names.add(tags.pop(k))
    if name:
        data['name'] = name
    if names:
        tags['names'] = list(names)
    if address:
        data['address'] = address
    if official_names:
        tags['official_names'] = list(official_names)
    data['tags'] = tags
    return data


def _shape_element(element):
    document = {}
    fields = element.attrib.keys()
    document['type'] = element.tag
    document['created'] = {k: element.attrib.get(k) for k in CREATED}

    # node & way
    tags = {}
    node_refs = []
    # members = []
    for child in element:
        if child.tag == 'tag':
            tags[child.attrib['k']] = child.attrib['v']
        elif child.tag == 'nd':
            node_refs.append(child.attrib['ref'])

    if tags:
        tags = _clean_tags(tags)
        document.update(tags)

    # way
    if node_refs:
        document['node_refs'] = node_refs

    # node
    if 'lat' in fields and 'lon' in fields:
        document['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]

    # other fields
    other_fields = set(fields) - set(CREATED) - {'lat', 'lon'}
    for k in other_fields:
        document[k] = element.attrib[k]

    return document


def shape_element(element):
    if element.tag in ['node', 'way']:
        return _shape_element(element)


def process_map(file_in, pretty=False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


if __name__ == "__main__":
    process_map(OSM_FILE, pretty=True)