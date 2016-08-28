from django.shortcuts import render, HttpResponse
import oauth2client.client as oauthClient
from settings import SPOTIFY_SECRET, CALENDAR_SECRET
import json

# Create your views here.
def oauth2callback_calendar(request):
	print request.body	# DEBUG
	calendar_secrets = json.loads( open(CALENDAR_SECRET) )
	try:
		flow = oauthClient.flow_from_clientsecrets(
			CALENDAR_SECRET,
			scope = calendar_secrets['web']['scope'],
			redirect_uri = calendar_secrets['web']['redirect_uris']
		)
		flow.params['access_type'] = 'offline'
	except:
		msg = 'There is an error with your calendar API tokens! Please review the credentials.'
		print msg	#DEBUG

	if 'code' not in request.body:
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
	else:
		auth_code = request.body['code']
		credentials = flow.step2_exchange(auth_code)
		# save credentials somewhere

	return redirect('login/client_id=calendar/')

def oauth2callback_spotify(request):
	print request.body	# DEBUG
	spotify_secrets = json.loads( open(CALENDAR_SECRET) )
	try:
		flow = oauthClient.OAuth2WebServerFlow(
			client_id = spotify_secrets['web']['client_id'],
			client_secret = spotify_secrets['web']['client_secret'],
			scope = spotify_secrets['web']['scope'],
			redirect_uri = spotify_secrets['web']['redirect_uris']
		)
		flow.params['access_type'] = 'offline'
	except:
		msg = 'There is an error with your spotify API tokens! Please review the credentials.'
		print msg	#DEBUG

	if 'code' not in request.body:
		auth_uri = flow.step1_get_authorize_url()
		return redirect(auth_uri)
	else:
		auth_code = request.body['code']
		credentials = flow.step2_exchange(auth_code)
		# save credentials somewhere

	return redirect('login/client_id=spotify/')

def adduser(request):
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(new_user)
            # redirect, or however you want to get to the main view
            return redirect("/login/calendar")
    else:
        form = UserForm() 

    return render(request, 'adduser.html', {'form': form}) 

