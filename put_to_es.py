import re, sys, json

import requests

import secrets



def do_request(method, endpoint, data=None):
    resp = getattr(requests, method)(
        '{}/stackexchange{}'.format(secrets.root_url, endpoint), data=json.dumps(data))
    print 'status:', resp.status_code
    print 'text:', resp.text


def put(endpoint, data=None):
    return do_request('put', endpoint, data=data)


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
    put('/so_post/_mapping', data)


def put_doc(doc_dict):
    put('/so_post/{}'.format(doc_dict['Id']), data=doc_dict)


def each_row(path):
  with open(path) as f:
    chunk = ''
    while True:
      new_data = f.read(1024)
      if not new_data:
        break
      chunk += new_data
      while True:
        match = re.search('<row.+?/>', chunk)
        if match:
          kv_strs = re.findall('[a-zA-Z]+=".+?"', match.group())
          kv_pairs = [kv_str.split('=', 1) for kv_str in kv_strs]
          kv_pairs = [(p[0], p[1][1:-1]) for p in kv_pairs]
          yield dict(kv_pairs)
          chunk = chunk[match.end():]
        else:
          break


if __name__ == "__main__":
    print 'loading tree...'
    for row_dict in each_row(sys.argv[1] if len(sys.argv) == 2 else 'test.xml'):
      put_doc(row_dict)
