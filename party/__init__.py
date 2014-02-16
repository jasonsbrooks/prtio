# import sys,os.path
# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rdio import Rdio
import pdb
import json
from urllib2 import HTTPError
import os
from random import randint

RDIO_CONSUMER_KEY = os.environ['RDIO_CONSUMER_KEY']
RDIO_CONSUMER_SECRET = os.environ['RDIO_CONSUMER_SECRET']
rdio = Rdio((RDIO_CONSUMER_KEY,RDIO_CONSUMER_SECRET))

def gettrackinfo(query):
    try:
        myResults = rdio.call('searchSuggestions', {'query':query, 'types': 'Track'})
    except HTTPError, e:
        print e.read()
        return None
    # pdb.set_trace()
    if myResults['result'] == []:
        return None

    myResults = myResults['result'][0]

    return [myResults['key'],myResults['name'],myResults['artist'],myResults['album'],myResults['icon']]

def getRandomTrack():
    try:
        myResults = rdio.call('getTopCharts', {'type': 'Track', 'count': 100})
    except HTTPError, e:
        print e.read()
        return None

    if myResults['result'] == []:
        return None

    return myResults['result'][randint(0,99)]['key']

