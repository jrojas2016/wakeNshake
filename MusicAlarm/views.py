from django.shortcuts import render, HttpResponse
from oauth2client.client import OAuth2Credentials
from apiclient.discovery import build
from spotipy import client
import httplib2
import json
import os

# Util functions
def get_cred(clientName):
	if clientName == 'spotify_cred':
		clientCreds = json.load( open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json', 'r') )
		clientCred = json.loads( clientCreds[clientName] )
		print type(clientCred) 	# DEBUG
		return clientCred['access_token']
	else:
		clientCreds = json.load( open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json', 'r') )
		clientCred = clientCreds[clientName]
		print type(clientCred)	# DEBUG
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
	# Spotify Requests #
	spotifyCred = get_cred('spotify_cred')
	# print spotifyCred 	# DEBUG
	spotifyClient = client.Spotify( auth = spotifyCred )
	playlists = spotifyClient.user_playlists( user = '122632253')	# spotify:user:122632253
	# print playlists 	# DEBUG

	# Calendar Requests #
	# calendarCredJson = get_cred('calendar_cred')
	# calendarCred = OAuth2Credentials().from_json(calendarCredJson)

	# http = httplib2.Http()
	# http = calendarCred.authorize(http)
	# service = build('calendar', 'v3', http=http)
	
	events = []

	return render(request, "dashboard.html", playlists = playlists['items'], events = events)
