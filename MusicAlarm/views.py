from django.shortcuts import render, HttpResponse
from oauth2client.client import OAuth2Credentials
from apiclient.discovery import build
from spotipy import client

from Crypto.Cipher import AES
from Crypto import Random
import httplib2
import datetime
import json
import os

# Util
class CryptoEngine:	# Don't know where is best to include this

	def __init__(self, key=b'Sixteen byte key'):
		self.key = key	# TODO: key generation/storage
		self.iv = Random.new().read(AES.block_size)
		self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)

	def decrypt_cred(self, encryptedCred):
		return self.cipher.decrypt(encryptedCred.decode("hex"))[len(self.iv):]

	def encrypt_cred(self, unencryptedCred):
		self.msg = self.iv + self.cipher.encrypt(unencryptedCred)
		return self.msg.encode("hex")

def get_cred(clientName):
	ce = CryptoEngine()
	if clientName == 'spotify_cred':
		clientCreds = json.load( open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json', 'r') )
		clientCred = json.loads( ce.decrypt_cred(clientCreds[clientName]) )
		print type(clientCred) 	# DEBUG
		return clientCred['access_token']
	else:
		clientCreds = json.load( open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json', 'r') )
		clientCred = str( ce.decrypt_cred(clientCreds[clientName]) )
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
