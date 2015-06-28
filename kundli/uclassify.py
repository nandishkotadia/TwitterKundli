import json
import requests

def uclassify(text):
    readkey = 'o6wS5h369a5z'
    payload = { 'readkey' : readkey , 'text' : text , 'output' : 'json' , 'version' : '1.01'}
    url = 'http://uclassify.com/browse/uClassify/' + 'topics' + '/ClassifyText'
    r = requests.get(url, params = payload)
    json_object = r.json()
    # print json_object
    # print r.text
    max_value = 0.0
    max_topic = ''
    for topic in json_object['cls1']:
        value = json_object['cls1'][topic]
        if value > max_value:
            max_value = value
            max_topic = topic
    return max_topic