import json

import xmltodict
import requests

import secrets


def put(endpoint, data=None):
    resp = requests.put(
        '{}/stackexchange{}'.format(secrets.root_url, endpoint), data=json.dumps(data))
    print 'status:', resp.status_code
    print 'text:', resp.text


def put_settings():
    data = {
        "analysis": {
            "analyzer": {
                "html_text": {
                    "tokenizer": "standard",
                    "filter": ["standard", "lowercase", "stop", "snowball"],
                    "char_filter": ["html_strip"]
                }
            }
        }
    }
    put('/_settings', data)


def put_mappings():
    data = {
        "so_post": {
            "properties": {
                "Body": {"type": "string",
                         "store": "yes",
                         "index_analyzer": "html_text"},
                "Id": {"type": "string",
                       "store": "yes"}
            }
        }
    }
    put('/so_post/_mapping'.format(secrets.root_url), data)


def put_doc(doc_dict):
    doc = {"Body": doc_dict['@Body'], "Id":  doc_dict['@Id']}
    put('/so_post/{}'.format(doc_dict['@Id']), data=doc)


class g:
    count = 10
def xml_item_callback(_, outer_doc_dict):
    if g.count <= 0:
        return False
    print 'count:', g.count
    g.count -= 1
    for doc_dict in outer_doc_dict['row']:
        put_doc(doc_dict)
    return True

if __name__ == "__main__":
    put('') # create index
    print 'loading tree...'
    with open('test.xml') as f:
        tree = xmltodict.parse(f, item_depth=1, item_callback=xml_item_callback)
    # requests.post('http://localhost:9200/stackexchange/_close')
    # createCustomAnalyzer()
    # createMappings()
    # requests.post('http://localhost:9200/stackexchange/_open')


# Adapted from:  https://github.com/o19s/StackExchangeElasticSearch/blob/master/postToEs.py
