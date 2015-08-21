from django.shortcuts import render
from django.http import HttpResponse
import json
import requests
from requests_oauthlib import OAuth1
from mood import mood
from uclassify import uclassify
from dateutil.tz import tzoffset
import re
import collections
import time
import datetime
import pprint
from utils import *
from itertools import cycle
import operator
from django.template import RequestContext
from django.shortcuts import render_to_response
# Create your views here.

API_ID = 'KQRNLy8L4t8dQ4Loay0N1cGJV'
API_SECRET = 'lFi8oSsnR2NsHZUkArGFNx4IMa2unFTTxJm4zRWkC7fd9WlKKr'
OAUTH_TOKEN = '837804571-OORMT78jbTrbrgiLk2HYKIWyEblUuZN94PWub1pN'
OAUTH_TOKEN_SECRET = 'QMB9fvepUud1p8ykK68Ye3O0WfSzWeGfn9WQJbWhqJu08'

API_ID_2 = '0DiP1RTBPv6BTE36YsIUHQ'
API_SECRET_2 = 'a56Wr9T6EvuaJvBQkaYyJZhq2qTaGfwl1l8O1a2P0uI'
OAUTH_TOKEN_2 = '17062577-JEXVIHGYcLjsm339u7Kb0GhTSBVJMn93Hxqh0BNRo'
OAUTH_TOKEN_SECRET_2 = 'OBfJSCWDXmSUGkxKWfbU95e67eAvfSWEs904rNb3voKpP'

MEGA_COUNT = 20

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

def home(request):
    if request.GET:
        username = request.GET.get('username')
        return render_to_response("home.html",{'username':username},context_instance=RequestContext(request))

TIMELINE_URI = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

def init_api(request):
    if request.GET:
        username = request.GET.get('username')

        URI_1 = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
        URI_2 = 'https://api.twitter.com/1.1/statuses/home_timeline.json'
        URI_4 = 'https://api.twitter.com/1.1/friends/ids.json'
        URI_5 = 'https://api.twitter.com/1.1/followers/ids.json'

KEY1 = ['KQRNLy8L4t8dQ4Loay0N1cGJV','lFi8oSsnR2NsHZUkArGFNx4IMa2unFTTxJm4zRWkC7fd9WlKKr','837804571-OORMT78jbTrbrgiLk2HYKIWyEblUuZN94PWub1pN','QMB9fvepUud1p8ykK68Ye3O0WfSzWeGfn9WQJbWhqJu08']
KEY2 = ['0DiP1RTBPv6BTE36YsIUHQ','a56Wr9T6EvuaJvBQkaYyJZhq2qTaGfwl1l8O1a2P0uI','17062577-JEXVIHGYcLjsm339u7Kb0GhTSBVJMn93Hxqh0BNRo','OBfJSCWDXmSUGkxKWfbU95e67eAvfSWEs904rNb3voKpP']
KEY3 = ['x64DkaSQAq3PqWlD2j2CBA','4f2Vf208osnvHE1TDfE7RXni2Ip6fQboOudHdTtE','17062577-2KZL6ZlRQ7S0nOS7INZj39j8HrtUjQrs3vt4PmATQ','8iegmh94XYt6bInFqMnP5ULIhP15vwsXN758TpaaVci9z']
KEY4 = ['njtMWSxd6WgYFJWrgYW6Kg','z5upcGYZeKYXi5VkttKuymSS2jI7wf7mVL1qRm050A','430556882-wGpXEPfWjRKzxGioJkMkdcZErC6IwLKqDSue51Bo','IDhIQjkQ3Vwlq3DtcuuZFdYb5GjKTbHULkK5n5ZtCPQy6']
KEY5 = ['hMNKDI1bkd8DRiCk3XbT8ly6L','2aFi0NyY01hHjr290mAUIwMzvPDH2idl55ebUuxXF6HGfqgKMQ','120086028-c0xEf3rTZLkawwG69CnTanzDY1pLXCwhN1FEKqX6','QoFwlRFcWzouoh0CI4VOAIZugCvl3IhOMQNGQMBfhWFAR']
KEY6 = ['Upwy7s3ZALjNiViX3g6NzNcYu','FlqR53ljbAorWsg92JH8CT9qIu1bJK60KxW7SLThTqSXwXybTO', '3258604662-7AapfCkY4kMDBCTr7jUtJSqLc9AxRqliZ2zPBtO','gLQBUxIqcecE12pDSrekuO0ZFWZc57t3yMtSPikVQsRI5']
KEY7 = ['t29n0eB0sdPZXykSFEjLGw','Ok6WXoMovlHCMCQgbBdIbjAyaRlZz1qdslthlAhXnpY','17062577-AwYInjHlxpXvmq4PTTX5VPt6GX0wpB7Dg5HASTYBN','uVarPsESzkOU2snUdey67S1fqhkVREa71T5zi4ltv3uH9']

def sentiment(request):
    if request.GET:
        username = request.GET.get('username')
        payload = {'screen_name' : username, 'count' : 25}
        auth = OAuth1(KEY2[0], KEY2[1],
                  KEY2[2], KEY2[3])
        r = requests.get(TIMELINE_URI,params=payload, auth=auth)
        abc = r.json()
        final_scores = []
        for i in abc:
            re.sub(r'[^\x00-\x7F]+',' ', i['text'])
            try:
                final_scores.append(mood(i['text'].decode('utf8')))
            except:
                pass
        return HttpResponse(json.dumps(final_scores))

    return HttpResponse("Oops")


def topics_hear_about(request):
    NEW_URI = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    if request.GET:
        username = request.GET.get('username')

        payload = {'screen_name' : username, 'count' : MEGA_COUNT}

        auth = OAuth1(KEY2[0], KEY2[1],
                  KEY2[2], KEY2[3])

        r = requests.get(NEW_URI,params=payload, auth=auth)

        abc = r.json()

        freq = collections.defaultdict(lambda: 0)

        for i in abc:
            re.sub(r'[^\x00-\x7F]+',' ', i['text'])
            freq[uclassify(i['text'])] += 1

        freq=sorted(freq.items(), key=operator.itemgetter(1), reverse=True)

        return HttpResponse(json.dumps(freq))

    return HttpResponse("Oops")

def topics(request):
    #topics i like to talk about
    if request.GET:
        username = request.GET.get('username')
        payload = {'screen_name' : username, 'count' : MEGA_COUNT}
        auth = OAuth1(KEY3[0], KEY3[1],
                  KEY3[2], KEY3[3])

        r = requests.get(TIMELINE_URI,params=payload, auth=auth)

        abc = r.json()

        freq = collections.defaultdict(lambda: 0)

        for i in abc:
            re.sub(r'[^\x00-\x7F]+',' ', i['text'])
            freq[uclassify(i['text'])] += 1

        freq=sorted(freq.items(), key=operator.itemgetter(1), reverse=True)

        return HttpResponse(json.dumps(freq))

    return HttpResponse("Oops")


def sleep_pattern(request):
    if request.GET:
        username = request.GET.get('username')
        payload = {'screen_name' : username, 'count' : MEGA_COUNT}
        auth = OAuth1(KEY4[0], KEY4[1],
                  KEY4[2], KEY4[3])

        r = requests.get(TIMELINE_URI,params=payload, auth=auth)
        tweets = r.json()

        freq = []

        for i in range(1,25):
            freq.append(0)

        for tweet in tweets:
            ts = time.strptime(tweet['created_at'], "%a %b %d %H:%M:%S +0000 %Y")
            freq[int(convert_time(ts.tm_hour,tweet['user']['utc_offset']))] += 1

        minm = 100000
        minsthour = 0
        maxsthour = 0
        maxm = 0

        for i in range(0,24):
            sumx = freq[cp(i)]+freq[cp(i+1)]+freq[cp(i+2)]+freq[cp(i+3)]+freq[cp(i+4)]+freq[cp(i+5)]+freq[cp(i+6)] + freq[cp(i+7)] + freq[cp(i+8)]
            # print "from "+str(cp(i))+" to "+str(cp(i+8)) + "is "+ str(sumx)
            minm = min(minm,sumx)
            maxm = max(maxm,sumx)
            if maxm == sumx:
                maxsthour = i
            if minm == sumx:
                minsthour = i

        # print "you sleep between" + str(cp(minsthour))+ " hours and " +str(cp(minsthour+8))
        # print "you tweet likely" + str(cp(maxsthour))+ " hours and " +str(cp(maxsthour+8))

        response = [{'sleep': [str(cp(minsthour)),str(cp(minsthour+8))], 'likely' : [str(cp(maxsthour)),str(cp(maxsthour+8))] }]

        return HttpResponse(json.dumps(response))

    return HttpResponse("false")


def cp(p):
    return (p+1)%24


def top_tweets(request):
    if request.GET:
        username = request.GET.get('username')
        payload = {'screen_name' : username, 'count' : 25}
        auth = OAuth1(KEY1[0], KEY1[1],
                  KEY1[2], KEY1[3])

        r = requests.get(TIMELINE_URI,params=payload, auth=auth)
        tweets = r.json()

        rtcount={}
        influenced_by = {}

        for tweet in tweets:
            # print 'Tweet id : ' + str(tweet['id']) + '  retweet count : ' + str(tweet['retweet_count'])
            # print tweet['retweeted']
            if tweet['text'].startswith('RT'):
                continue
            rtcount[tweet['text']] = tweet['retweet_count']

        # print rtcount

        rtcount=sorted(rtcount.items(), key=operator.itemgetter(1), reverse=True)

        toptweets_json=json.dumps(rtcount)

        return HttpResponse(toptweets_json)

    return HttpResponse("false")


def get_profile(request):
    if request.GET:
        username = request.GET.get('username')
        payload = {'screen_name' : username}
        auth = OAuth1(KEY1[0], KEY1[1],
                  KEY1[2], KEY1[3])

        K_URI = "https://api.twitter.com/1.1/users/show.json"

        r = requests.get(K_URI,params=payload, auth=auth)
        return HttpResponse(r.text)

    return HttpResponse("false")

def get_interest(request):
    P_URI = 'https://api.twitter.com/1.1/friends/ids.json'
    if request.GET:

        username = request.GET.get('username')

        payload = {'screen_name' : username,'count': MEGA_COUNT}
        auth = OAuth1(KEY5[0], KEY5[1],
                  KEY5[2], KEY5[3])
        r = requests.get(P_URI,params=payload, auth=auth)

        abc = r.json()

        users= abc['ids']

        url= "https://api.twitter.com/1.1/users/show.json"

        interests={}
        children={}

        for ids in users:
            payload={'user_id':ids}
            r = requests.get(url,params=payload,auth=auth)
            xyz=r.json()
            name=xyz['screen_name']
            topic=uclassify(xyz['description'])
            # print "Name:", str(name), " Interest:", str(topic)

            if interests.has_key(topic):
                interests[topic]= interests[topic] + "," + name
            else:
                interests[topic]=name

    return HttpResponse(json.dumps(interests))

def get_graph(request):

    URILL = 'https://api.twitter.com/1.1/friends/ids.json'

    if request.GET:

        username = request.GET.get('username')
        payload = {'screen_name' : username,'count': 20}
        auth = OAuth1(KEY6[0], KEY6[1], KEY6[2], KEY6[3])

        r = requests.get(URILL,params=payload, auth=auth)

        abc = r.json()

        users= abc['ids']

        url= "https://api.twitter.com/1.1/users/show.json"

        interests={}
        children={}
        data={}

        for ids in users:
            payload={'user_id':ids}
            r = requests.get(url,params=payload,auth=auth)

            xyz=r.json()

            name=xyz['screen_name']
            topic=uclassify(xyz['description'])
            # print "Name:", str(name), " Interest:", str(topic)

            if interests.has_key(topic):
                interests[topic]= interests[topic] + "@" + name
            else:
                interests[topic]=name

        for temp in interests.keys():
            data[temp]=username

        # print interests
        # print data
        for key in interests.keys():
            temp=interests[key]
            # print temp
            temp1=temp.split('@')
            # print temp1
            for temp2 in temp1:
                 data[temp2]=key

        # print json.dumps(interests)
        # print '\n\n'
        # print data
        # data=sorted(data.items(), key=operator.itemgetter(1))
        return HttpResponse(json.dumps(data))


def get_location(request):

    URIX = 'https://api.twitter.com/1.1/followers/ids.json'
    # 25
    if request.GET:
        username = request.GET.get('username')
        payload = {'screen_name' : username,'count': 15}
        auth = OAuth1(KEY7[0], KEY7[1],
                  KEY7[2], KEY7[3])
        r = requests.get(URIX,params=payload, auth=auth)

        abc = r.json()

        users = abc['ids']

        location = []

        for i in users[:15]:
            url = "https://api.twitter.com/1.1/users/show.json"
            payload = {'user_id':i}

            auth= OAuth1(API_ID, API_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

            r = requests.get(url,params=payload,auth=auth)

            xyz = r.json()

            if xyz['location'] != "":
                location.append(xyz['location'])

        return HttpResponse(json.dumps(location))