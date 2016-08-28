from django.shortcuts import render, HttpResponse

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
	return render(request, "dashboard.html")
