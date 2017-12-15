# -*- coding: utf-8 -*-

import re
from pprint import pprint
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")

db = client.test

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


# list all postcode
def audit_postcode():
    result = db.shanghai.aggregate([
        {'$match': {'address.postcode': {'$exists': 1}}},
        {'$group': {
            '_id': '$address.postcode',
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}},
        # {'$limit': 10}
    ])
    for item in result:
        pprint(item)


# list all tag keys, and check
def audit_tag_keys():
    result = db.shanghai.find({'tags': {'$exists': 1}})
    keys = set()
    for item in result:
        tags = item['tags']
        keys.update(tags.keys())

    for k in sorted(list(keys)):
        print k
        if problemchars.search(k):
            print k


# list amenity
def audit_tag_amentiy():

    result = db.shanghai.aggregate([
        {'$group': {
            '_id': '$tags.amenity',
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}},
        # {'$limit': 10}
    ])

    for item in result:
        pprint(item)

# list


# list phone
def audit_tag_phone():
    result = db.shanghai.find({'tags.phone': {'$exists': 1}})
    phone = set()
    for item in result:
        phone.add(item['tags']['phone'])

    for a in phone:
        print a


# how many phone:
def count_tags():
    result = db.shanghai.find({'tags': {'$exists': 1}})
    phone = set()
    for item in result:
        phone.add(item['tags']['phone'])

    for a in phone:
        print a


# 再看看其他的tag，有什么好玩的，统计一下属性出现最多的是哪些

# 看看 highway, building, source, oneway, power, bridge, lanes, layer, ref, created_by, natural, landuse, amenity, waterway
# railway, height, service, network,
#

def audit_tag_attrib():
    result = db.shanghai.aggregate([
        {'$match': {'tags.amenity': {'$exists': 1}}},
        {'$group': {
            '_id': '$tags.amenity',
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ])

    for item in result:
        # print item['_id']
        pprint(item)

# 看看user
def audit_tag_user():

    result = db.shanghai.aggregate([
        {'$group': {
            '_id': {'uid': '$created.uid', 'user':'$created.user'},
            'source': {'$addToSet': '$tags.source'},
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ])
    for item in result:
        pprint(item)

# 看看user
def audit_user_contribute():

    result = db.shanghai.aggregate([
        {'$group': {
            '_id': {'uid': '$created.uid', 'user': '$created.user'},
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}},
        {'$limit': 5}
    ])
    for item in result:
        pprint(item)

# 实际有多少不重复的名字
# def audit_way_names():
#     result = db.shanghai.aggregate([
#         {'$match': }
#         {'$group': {
#             '_id': {'uid': '$created.uid', 'user': '$created.user'},
#             'count': {'$sum': 1}
#         }},
#         {'$sort': {'count': -1}},
#         {'$limit': 5}
#     ])
#     for item in result:
#         pprint(item)


# user contribute only once
def audit_user_once_contribute():
    result = db.shanghai.aggregate([
        {'$group': {
            '_id': {'uid': '$created.uid', 'user': '$created.user'},
            'count': {'$sum': 1}
        }},
        {'$match': {'count': 1}},
        {'$group': {
            '_id': 'number_of_users_contribute_once',
            'count': {'$sum': 1}
        }},
    ])
    for item in result:
        pprint(item)

# 看看创建时间 按年统计
# 时间的问题。


def audit_created():
    result = db.shanghai.aggregate([
        {'$project': {
            '_id': '$_id',
            'year': {'$substr': ['$created.timestamp', 0, 4]},
        }},
        {'$group': {
            '_id': '$year',
            'count': {'$sum': 1}
        }},
        {'$sort': {'count': -1}},
        # {'$limit': 10}
    ])
    for item in result:
        pprint(item)


# 年度贡献最多的人
def audit_contribute():
    result = db.shanghai.aggregate([
        {'$group': {
            '_id': {
                'year': {'$substr': ['$created.timestamp', 0, 4]},
                'uid': '$created.uid',
                'user': '$created.user'
            },
            'count': {'$sum': 1}
        }},
        {'$group': {
            '_id': '$_id.year',
            'max': {'$max': '$count'},
            'total': {'$sum': '$count'},
            'user': {'$push': {'uid': '$_id.uid', 'user': '$_id.user', 'count': '$count'}},
        }},
        {'$unwind': '$user'},
        {'$project': {
            '_id': '$_id',
            'count': '$user.count',
            '_diff': {'$subtract': ['$user.count', '$max']},
            'ratio': {'$divide': ['$user.count', '$total']},
            'uid': '$user.uid',
            'total': '$total',
            'user': '$user.user',
        }},
        {'$match': {'_diff': 0}},
        {'$sort': {'_id': -1}}
    ])
    for item in result:
        pprint(item)


# 看看 id是否唯一
def audit_id():
    result = db.shanghai.aggregate([
        {'$group': {
            '_id': '$id',
            'count': {'$sum': 1},
            'versions': {'$push': '$created.user'}
        }},
        {'$match': {'count': {'$gt': 1}}}
    ])
    for item in result:
        pprint(item)

# 是否有name属性
def audit_name():
    print 'tatal',
    print db.shanghai.count()
    print 'name exists',
    print db.shanghai.find({'name': {'$exists': 1}}).count()
    print db.shanghai.find({'type': 'node'}).count(),
    print db.shanghai.find({'type': 'node', 'name': {'$exists': 1}}).count()
    print db.shanghai.find({'type': 'way'}).count(),
    print db.shanghai.find({'type': 'way', 'name': {'$exists': 1}}).count()
    print db.shanghai.find({'type': 'relation'}).count(),
    print db.shanghai.find({'type': 'relation', 'name': {'$exists': 1}}).count()
    print 'tag exists',
    print db.shanghai.find({'tags': {'$exists': 1}}).count()
    # for item in result:
    #     pprint(item)

if __name__ == '__main__':
    audit_tag_attrib()