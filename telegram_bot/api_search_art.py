#! python

import requests
from pprint import pprint
import random

token = "12775826-547199fe80cd4b41906433e2c"

def_query = "https://pixabay.com/api/?key=12775826-547199fe80cd4b41906433e2c&q=yellow+flowers&image_type=photo"


class PixGetter:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://pixabay.com/api/?key={}/".format(token)
        self.type = "&image_type=photo"

    def get_pix(self, query):
        method = '&q='
        j = self.api_url + method + query + self.type
        print(j)
        resp = requests.get(self.api_url + method + query + self.type)
        result_json = resp.json()
        x = random.randrange(0, len(result_json['hits']))
        return result_json['hits'][x]['webformatURL']



if __name__ == "__main__":
    pix = PixGetter(token)
    jsn = pix.get_pix("Cute girl")
    pprint(jsn)