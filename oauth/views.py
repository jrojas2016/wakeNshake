from settings import SPOTIFY_SECRET, CALENDAR_SECRET
from django.shortcuts import render, HttpResponse
import oauth2client.client as oauthClient
import hashlib
import json

# Util Functions
def sha512_hash(credentials):
	shaCred = hashlib.sha512(credentials).hexdigest()
	return shaCred

# Create your views here.
def oauth2callback_calendar(request):
	print request.body	# DEBUG
	calendarSecrets = json.loads( open(CALENDAR_SECRET) )
	try:
		flow = oauthClient.flow_from_clientsecrets(
			CALENDAR_SECRET,
			scope = calendarSecrets['web']['scope'],
			redirect_uri = calendarSecrets['web']['redirect_uris']
		)
		flow.params['access_type'] = 'offline'
	except:
		msg = 'There is an error with your calendar API tokens! Please review the credentials.'
		print msg	#DEBUG

	if 'code' not in request.body:
		authUri = flow.step1_get_authorize_url()
		return redirect(authUri)
	else:
		authCode = request.body['code']
		credentials = flow.step2_exchange(authCode)
		shaCred = sha512_hash(credentials.to_json())
		# update user entry in db

	return redirect('login/client_id=calendar/')

def oauth2callback_spotify(request):
	print request.body	# DEBUG
	spotifySecrets = json.loads( open(CALENDAR_SECRET) )
	try:
		flow = oauthClient.OAuth2WebServerFlow(
			client_id = spotifySecrets['web']['client_id'],
			client_secret = spotifySecrets['web']['client_secret'],
			scope = spotifySecrets['web']['scope'],
			redirect_uri = spotifySecrets['web']['redirect_uris']
		)
		# flow.params['show_dialog'] = False	# might not need
	except:
		msg = 'There is an error with your spotify API tokens! Please review the credentials.'
		print msg	#DEBUG

	if 'code' not in request.body:
		authUri = flow.step1_get_authorize_url()
		return redirect(authUri)
	else:
		authCode = request.body['code']
		credentials = flow.step2_exchange(authCode)
		shaCred = sha512_hash(credentials.to_json())
		# update user entry in db

	return redirect('login/client_id=spotify/')
