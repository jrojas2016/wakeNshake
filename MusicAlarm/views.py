from django.shortcuts import render, HttpResponse

# Create your views here.

def homeview(request):
	return render(request, "home.html")

def login(request, client_id):
	client = {"client_id": client_id}
	return redirect(request, "login.html", client = client)


