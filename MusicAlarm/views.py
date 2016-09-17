from django.shortcuts import render, HttpResponse
from oauth2client.client import OAuth2Credentials
from apiclient.discovery import build
from spotipy import client
import httplib2
import json
import os
import datetime
# Util functions
def get_cred(clientName):
	if clientName == 'spotify_cred':
		clientCreds = json.load( open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json', 'r') )
		clientCred = json.loads( clientCreds[clientName] )
		print type(clientCred) 	# DEBUG
		return clientCred['access_token']
	else:
		clientCreds = json.load( open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json', 'r') )
		clientCred = str( clientCreds[clientName] )
		print type(clientCred) 	# DEBUG
		return clientCred

# Create your views here.
def homeview(request):
	return render(request, "home.html")

def spotify_login(request):
	# client = {"client_id": 'spotify'}
	return render(request, "spotify_login.html")

def calendar_login(request):
	# client = {"client_id": 'calendar'}
	return render(request, "calendar_login.html")

def dashboard(request):

	# Query Params
	now = datetime.datetime.utcnow().isoformat() + '-07:00'	#California tz offset

	# Spotify Requests #
	spotifyCred = get_cred('spotify_cred')
	# print spotifyCred 	# DEBUG
	spotifyClient = client.Spotify( auth = spotifyCred )
	playlists = spotifyClient.user_playlists( user = '1248308979')	# spotify:user:122632253
	# print playlists 	# DEBUG

	# Calendar Requests #
	calendarCredJson = get_cred('calendar_cred')
	calendarCred = OAuth2Credentials.from_json(calendarCredJson)

	http = httplib2.Http()
	http = calendarCred.authorize(http)
	service = build('calendar', 'v3', http = http)
	events = service.events().list(
		calendarId = 'jrojas2016@gmail.com', 
		orderBy = "startTime",
		singleEvents = True, 
		maxResults = 10,
		timeMin = now
	).execute()
	# print events 	# DEBUG
	currenttime = datetime.datetime.now()
	print currenttime
	context = {'playlists': playlists['items'], 'events':events['items'], 'now':currenttime}
	return render(request, "dashboard.html", context)
