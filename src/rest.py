'''
Created on 1 Oct 2019
This tests the fact that I can use rest to interrogate GLTEN and return their json string

@author: castells
'''
import requests
import json
class APIError(Exception):
    """An API Error Exception"""

    def __init__(self, status):
        self.status = status

    def __str__(self):
        return "APIError: status={}".format(self.status)



if __name__ == '__main__':
    resp = requests.get('https://glten.org/api/v0/public/experiment/56')
    if resp.status_code != 200:
        # This means something went wrong.
        raise APIError('GET /tasks/ {}'.format(resp.status_code))
    #for todo_item in resp.json():
        #print('{} {}'.format(todo_item['id'], todo_item['summary']))
    strJsDoc =  json.dumps(resp.json(), indent=4)
    print(strJsDoc)