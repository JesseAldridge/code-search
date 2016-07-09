import json

import requests

import secrets


data = {
  "query" : {
    "query_string" : {
       "query" : "grid = "
    }
  }
}
resp = put_to_es.do_request('post', '{}/_search'.format(secrets.root_url), data)
print resp.content
