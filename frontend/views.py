from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def profile(request, username):
    return render(request, "profile.html", {"username": username})

def auth(request):
    return render(request, "auth.html")

@login_required
def feed(request):
    return render(request, "feed.html")
