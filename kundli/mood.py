from __future__ import division
import nltk
import numpy
from nltk.tokenize import *
import json
import re
import csv
import sys
import pickle
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import *
from collections import Counter
import socket
import sys
import os
module_dir = os.path.dirname(__file__)

def bigramReturner(tweetString):
    tweetString = tweetString.lower()
    # tweetString = removePunctuation (tweetString)
    bigramFeatureVector = []
    for item in nltk.bigrams(tweetString.split()):
        bigramFeatureVector.append(' '.join(item))
    return bigramFeatureVector


stemmer = SnowballStemmer("english")

stop = stopwords.words('english')
# ItemID,Sentiment,SentimentSource,SentimentText
#above is the order in which the tweetdataset columns are
#reading the csv file
#csvfile=open('untouched.csv','rb')
#reader= csv.reader(csvfile)

#unicode encoding stuff
reload(sys)
sys.setdefaultencoding('utf8')

#positive tweet words
pos_tweets = []
#negative tweet words
neg_tweets = []

#positive words and negative words
pos_words = []
neg_words = []

#pos_tags to rmove
pos_tags_to_remove = ['DT', 'PRP', 'PRP$', 'IN', 'CD', '-NONE-', 'WRB']
#pos_tags_to_remove=['NN','DT','NNS','PRP','PRP$','NNP','IN','MD','CD','NNPS','-NONE-']
#list of uselesswordsee
useless_words = ['just', 'very', 'too', 'im', 'amp', 'and', 'am', 'feel', 'is', 'are', 'was', 'for', 'any', 'got',
                 'now', 'http', 'tumblr', 'you', 'twitter', 'quot', 'woot', 'what', 'where', 'how', 'who', 'when',
                 'why']


def islessthan3(word):
    chararray = []
    chararray.extend(word)
    for char in chararray:
        if chararray.count(char) > 3:
            return False
    return True


def hasdigit(word):
    for i in word:
        if i.isdigit() or i in string.punctuation:
            return True
    return False


exclude = set(string.punctuation)

#preprocessing block
def preprocess(tweets):
    newarray = []
    m = tweets.count('not ')
    y = tweets.count('cant ')
    z = tweets.count('wont ')

    if m > 0 or y > 0 or z > 0:
        tweetarray = word_tokenize(tweets.lower())
        wordstoremove = ['not']
        bilist = bigramReturner(tweets)
        #print "detected bigram"
        for item in bilist:
            if (item.split()[0] == "not"):
                x = item.split()[1]
                #s = ''.join(ch for ch in x if ch not in exclude)
                wordstoremove.append(x)
                s = "!" + x
                newarray.append(s)
        for t in tweetarray:
            if t not in wordstoremove and len(t) > 2:
                newarray.append(t)
        return newarray


    else:
        tweetstoprocess = word_tokenize(tweets.lower())
        for feeling in tweetstoprocess:
            #removing links
            feeling = re.sub(r'^http?:\/\/.*[\r\n]*', '', feeling, flags=re.MULTILINE)
            feeling = re.sub(r'\w[&@]\w', '', feeling)
            feeling = re.sub(r'^&\w', '', feeling)
            feeling = re.sub(r'^@', '', feeling)
            feeling = re.sub(r'\w[; -]\w', '', feeling)
            feeling = re.sub(r'\w;', '', feeling)
            feeling = re.sub(r'^#\w', '', feeling)
            feeling = re.sub(r'[^\x00-\x7f]', r' ', feeling)
            #feeling=WordNetLemmatizer().lemmatize(feeling)
            temparray = []
            #feelingarray=word_tokenize(feeling.lower())
            #removing words less than 3
            #for feels in feelingarray:
            if len(feeling) > 2 and feeling not in useless_words and islessthan3(feeling) and not hasdigit(feeling):
                temparray = [feeling.lower()]
            #pos tagging words
            postagarray = nltk.pos_tag(temparray)
            #print postagarray
            for (postaggedword, tag) in postagarray:
                if tag not in pos_tags_to_remove:
                    newarray.append(str((postaggedword)))
        return newarray


posdict = pickle.load(open(os.path.join(module_dir, 'data/unipos100k.p'), "rb"))
negdict = pickle.load(open(os.path.join(module_dir, 'data/unineg100k.p'), "rb"))

posdict_bi = pickle.load(open(os.path.join(module_dir, 'data/bipos1m.p'), "rb"))
negdict_bi = pickle.load(open(os.path.join(module_dir, 'data/bineg1m.p'), "rb"))

positivedictionary = {}
positivedictionary.update(posdict)
positivedictionary.update(posdict_bi)

negativedictionary = {}
negativedictionary.update(negdict)
negativedictionary.update(negdict_bi)

num = 30000
numofpostweets = 15161
numofnegtweets = 14839
probofpos = numofpostweets / num
probofneg = numofnegtweets / num

Feararray = ['tensed', 'oh my god', 'omg', 'cold-feet', 'afraid', 'angst', 'anxious', 'apprehensive', 'cowardice',
             'doubt', 'dread', 'dreadful', 'fear', 'fearful', 'fearsome', 'flighty', 'fret', 'fright', 'frightful',
             'gutless', 'horror', 'jitters', 'kill', 'nervous', 'nightmare', 'panic', 'petrified', 'queasy', 'scare',
             'scared', 'scary', 'shitless', 'skittish', 'spooky', 'suspicion', 'terror', 'trembling', 'traumatic',
             'unease', 'uneasy', 'unpleasant', 'unquiet', 'worried', 'worry', 'wreck', 'shitless', 'cold feet',
             'scared shitless' 'kill me', 'freaking out', 'shit', ':o', 'shocked'];

Sadpersonalarray = ['down', 'happy', 'good', 'depressing', 'heartbreaking', 'sad', 'sorrow', 'unhappy', 'upset',
                    'alienated', 'pitiful', 'unpleasant', 'pain', 'lamentable', 'deplorable', 'sorry', 'glum', 'loss',
                    'lost', 'death', 'dying', 'cold', 'dark', 'pout', 'brooding', 'moody', 'melancholy', 'solemn',
                    'blue', 'gloomy', 'down', 'dismal', 'mournful', 'pessimistic', 'lost', 'somber', 'hollow',
                    'wistful', 'bereaved', 'chearless', 'dejected', 'gloomy', 'grief', 'sick', 'weeping', 'morbid',
                    'hurt', 'hurting', 'troubled', 'pensive', 'unpleasant', 'fucked', 'griefstricken', 'grieving',
                    'lonely', 'longing', 'sorrowful', 'victim', 'struck with grief', 'kill me now', 'low spirits',
                    'grief-stricken', 'long-faced', 'low-spirited', 'heart-breaking', 'life', 'tired', 'breakup',
                    'dump', 'dumped', 'broken up', 'heart breaking', 'troubling', 'beat', 'rough spot', 'rough-spot',
                    'shattered', 'bad'];

Angryarray = ['abrasive', 'angry', 'stupid', 'dumb', 'irritating', 'what the hell', 'hell', 'annoyed', 'antagonized',
              'antagonizing', 'ballistic', 'bitter', 'chagrin', 'contempt', 'crazy', 'disturbed', 'enraged', 'fuming',
              'furious', 'grudge', 'hateful', 'heated', 'insane', 'irritable', 'mad', 'peevish', 'pissed', 'scowl',
              'sore', 'storming', 'sullen', 'vexing', 'resent', 'resentful', 'sour', 'wrath', 'unbalanced', 'unhinged',
              'rage', 'offended', 'turbulent', 'outraged', 'snotty', 'bullshit', 'freakout', 'dirtylook', 'heated',
              'hotheaded', 'ill temepered', 'freak out', 'kill someone', 'dirty look', 'fired up', 'off the hook',
              'off the rails', 'worked up', 'hot headed', 'ill-tempered', 'freak-out', 'dirty-look', 'fired-up',
              'off-the-hook', 'off-the-rails', 'worked-up', 'hot-headed', 'ill temepered', 'freak out', 'kill someone',
              'dirty look', 'fired up', 'off the hook', 'off the rails', 'worked up', 'hot headed', 'ill-tempered',
              'freak-out', 'dirty-look', 'fired-up', 'off-the-hook', 'off-the-rails', 'worked-up', 'hot-headed',
              'angry', 'explode'];

Sadprofarray = ['not-a-winner', 'not a winner', 'too big', 'looking down', 'burn', 'catch22', 'crash', 'dejected',
                'demoralised', 'demoralized', 'dicey', 'disheartened', 'dismay', 'disappointed', 'disappointing',
                'dispirit', 'doubtful', 'doubting', 'fail', 'failure', 'farce', 'farrago', 'hodgepodge', 'loser',
                'mishmash', 'monotonous', 'unmotivated', 'uncertain', 'worry', 'work', 'boss', 'goals', 'troublesome',
                'trouble', 'life is getting nowhere', 'rut', 'getting nowhere', 'difficult to crack', 'implode',
                'succumb', 'breaking point', 'saturated', 'pushing my limits', 'target', 'sales'];

Depressedarray = ['suicide', 'suicidal', 'kill myself', 'dont want to live', 'depressed', 'distressed',
                  'jump out of the window', 'no reason to live', 'jump out the window']


def mood(tweet):
    #socket
    #conn,addr =s.accept()
    finalprobofpos = 1.0
    finalprobofneg = 1.0
    posnumerator = 1.0
    posdenominator = 1.0
    negnumerator = 1.0
    negdenominator = 1.0
    score = 0.0
    sentiment = ""
    #xinput = raw_input("enter your feeling:\n")
    #we remove user input and take input from php using socket
    #data=conn.recv(100000)
    #xinput=data.decode("utf-8")
    input = tweet.lower()
    #print "input : ",input
    #feeling = word_tokenize(input.lower())
    feel = preprocess(str(input))

    for w in feel:

        if w not in positivedictionary:
            cp = numofpostweets
        else:
            cp = positivedictionary[w]  #countpos(w)
        if w not in negativedictionary:
            cn = numofnegtweets
        else:
            cn = negativedictionary[w]  #countneg(w)
        '''
		cp=positivedictionary[w]
		cn=negativedictionary[w]
		'''
        posnumerator = posnumerator * (cp / len(posdict))  #numofpostweets)
        posdenominator = posdenominator * ((cp + cn) / num)

    if posdenominator == 0:
        posdenominator = 1
    finalprobofpos = posnumerator * (0.5 / posdenominator)

    #print "probability of being positive:",finalprobofpos

    negnumerator = 1.0
    negdenominator = 1.0
    for w in feel:

        if w not in positivedictionary:
            cp = numofpostweets
        else:
            cp = positivedictionary[w]  #countpos(w)
        if w not in negativedictionary:
            cn = numofnegtweets  #replaced with 0 ... as other words could still have some prob
        else:
            cn = negativedictionary[w]  #countneg(w)
        '''
		cp=positivedictionary[w]
		cn=negativedictionary[w]
		'''
        negnumerator = negnumerator * cn / len(negdict)  #numofnegtweets
        negdenominator = negdenominator * ((cn + cp) / num)

    if negdenominator == 0:
        negdenominator = 1
    finalprobofneg = negnumerator * (0.5 / negdenominator)


    #print "probability of being negative:",finalprobofneg

    if finalprobofneg < finalprobofpos:
        #senddata=conn.send("Happy")
        score = finalprobofpos
        #print "happy"
        sentiment = "happy"
    else:  #if detected negative we further classify
        flag = 0
        score = finalprobofneg * -1
        for depressedword in Depressedarray:
            if input.find(depressedword) != -1:
                #senddata=conn.send("Depressed")
                #print "depressed"
                sentiment = "depressed"
                flag = 1
                break
        for angryword in Angryarray:
            if input.find(angryword) != -1:
                #senddata=conn.send("Anger")
                #print "angry"
                sentiment = "angry"
                flag = 1
                break
        for sadprofword in Sadprofarray:
            if input.find(sadprofword) != -1:
                #senddata=conn.send("SadProf")
                #print "sadprofessional"
                sentiment = "sad professional"
                flag = 1
                break
        for sadpersonalword in Sadpersonalarray:
            if input.find(sadpersonalword) != -1:
                #senddata=conn.send("SadPersonal")
                #print "sadpersonal"
                sentiment = "sad personal"
                flag = 1
                break
        for fearword in Feararray:
            if input.find(fearword) != -1:
                #senddata=conn.send("Fear")
                #print "fear"
                sentiment = "fear"
                flag = 1
                break
        if flag == 0:
            #senddata=conn.send("SadPersonal")
            #print "sadpersonal"
            sentiment = "sad personal"

    #score calculation

    return (finalprobofpos,finalprobofneg)







