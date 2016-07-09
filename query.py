import json

import requests

import settings


data = {
  "query" : {
    "query_string" : {
       "query" : "grid = "
    }
  }
}
resp = requests.post('{}/_search'.format(settings.root_url), data=json.dumps(data))
print resp.content
