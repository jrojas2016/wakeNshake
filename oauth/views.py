from wakeNshake.settings import SPOTIFY_SECRETS, CALENDAR_SECRETS
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_protect
import oauth2client.client as oauthClient
import hashlib
import json
import os
from models import UserForm
from django.contrib.auth.models import User
from models import customUser
from django.contrib.auth import authenticate

class session:
	spotify_code = None
	calendar_code = None
	def __init__(self):
		pass

sesh = session()

# Util Functions
def sha512_hash(credentials):
	shaCred = hashlib.sha512(credentials).hexdigest()
	return shaCred

# Create your views here.
@csrf_protect
def oauth2callback_calendar(request):
	# current_user = request.user
	calendarSecrets = json.load( open(CALENDAR_SECRETS) )

	try:
		flow = oauthClient.flow_from_clientsecrets(
			CALENDAR_SECRETS,
			scope = calendarSecrets['web']['scope'],
			redirect_uri = 'http://localhost:8000/oauth2callback/calendar'
		)
		flow.params['access_type'] = 'offline'
	except:
		msg = 'There is an error with your calendar API tokens! Please review the credentials.'
		print msg	#DEBUG

	print request.GET.get('code', '')
	if request.GET.get('code', '') is '':
		authUri = flow.step1_get_authorize_url()
		return redirect(authUri)
	else:
		# customUser.objects.create(user= current_user )
		authCode = request.GET.get('code', '')
		print authCode
		session.calendar_code = authCode
		credentials = flow.step2_exchange(authCode)
		savedCred = json.load( open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json') )
		savedCred['calendar_cred'] = credentials.to_json()
		json.dump(savedCred, open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json', 'w') )
		# customUser.object.create(user= current_user, calendar_cred = credentials)
		# customUser.save()
		#shaCred = sha512_hash(credentials.to_json())
		# update user entry in db
	return redirect('calendar_login')

@csrf_protect
def oauth2callback_spotify(request, user):
	# current_user = request.user
	spotifySecrets = json.loads( open(SPOTIFY_SECRETS) )
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

	if 'spotify_code' not in session:
		authUri = flow.step1_get_authorize_url()
		return redirect(authUri)
	else:
		# cust = customUser.objects.get(user= current_user)
		authCode = request.GET.get('code', '')
		session['spotify_code'] = authCode
		credentials = flow.step2_exchange(authCode)
		savedCred = json.load( open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json') )
		savedCred['spotify_cred'] = credentials.to_json()
		json.dump(savedCred, open(os.getcwd() + '/oauth/ClientSecrets/clientCred.json', 'w') )
		#shaCred = sha512_hash(credentials.to_json())
		# cust.spotify_cred = credentials
		# cust.save()
		# update user entry in db
	return redirect('spotify_login')



# def adduser(request):
# 	print 'rendered'
# 	form = UserForm(request.POST)
# 	if form.is_valid():
# 		new_user = User.objects.create_user(**form.cleaned_data)
# 		new_user.save()
# 		# redirect, or however you want to get to the main view
# 		user = new_user
# 		user.save()
# 		print "User is valid"
# 		client = {}
# 		print user.username
# 		auth_user = authenticate( username = user.username, password = user.password)
# 		print auth_user
# 		if auth_user is not None:
# 			login(request, user)
# 		else:
# 			pass
# 		return render(request, 'calendar_login.html', {'user': user} )
# 	else:
# 		form = UserForm() 
# 		print "User is not valid"


# 	return render(request, 'adduser.html', {'form': form}) 

