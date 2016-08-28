from django.shortcuts import render, HttpResponse

# Create your views here.

def homeview(request):
	return render(request, "home.html")

def account_creation(request, client_id):
	client = {"client_id": client_id}
	return redirect(request, "account_creation.html", client = client)

def login(request):
	return render(request, "login.html")

