#! /usr/bin/env python

import sys,os.path
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rdio import Rdio
import pdb
import json
from rdio_consumer_credentials import RDIO_CREDENTIALS
from urllib2 import HTTPError

rdio = Rdio(RDIO_CREDENTIALS)

def gettrackinfo(query):
	try:
		myResults = rdio.call('searchSuggestions', {'query':query, 'types': 'Track'})
	except HTTPError, e:
		print e.read()

	if myResults['result'] == []:
		return None

	myResults = myResults['result'][0]

	# print [myResults['key'],myResults['name'],myResults['albumArtist']]
	return [myResults['key'],myResults['name'],myResults['albumArtist']]

def gettrackid(query):
	try:
		myResults = rdio.call('searchSuggestions', {'query':query, 'types': 'Track'})
	except HTTPError, e:
		print e.read()

	if myResults['result'] == []:
		return None

	myResults = myResults['result'][0]

	return myResults['key']







