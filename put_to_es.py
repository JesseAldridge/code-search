import json

import xmltodict
import requests

import settings


def put(endpoint, data=None):
    resp = requests.put(
        '{}/stackexchange{}'.format(settings.root_url, endpoint), data=json.dumps(data))
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
                # Each type has different configuration
                # settings here, string is the most
                # important
                # mapping > types > core types
                "Body": {"type": "string",
                         "store": "yes",
                         "index_analyzer": "html_text"},
                "Id": {"type": "string",
                       "store": "yes"}
            }
        }
    }
    put('/so_post/_mapping'.format(settings.root_url), data)


def put_doc(doc_dict):
    doc = {"Body": doc_dict['@Body'], "Id":  doc_dict['@Id']}
    put('/so_post/{}'.format(doc_dict['@Id']), data=doc)


if __name__ == "__main__":
    with open('test.xml') as f:
        tree = xmltodict.parse(f.read())
    put('')  # create index
    # requests.post('http://localhost:9200/stackexchange/_close')
    # createCustomAnalyzer()
    # createMappings()
    # requests.post('http://localhost:9200/stackexchange/_open')

    for doc_dict in tree['posts']['row']:
        put_doc(doc_dict)


# Adapted from:  https://github.com/o19s/StackExchangeElasticSearch/blob/master/postToEs.py
