from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from sso.models import User

# Create your views here.

@login_required(login_url="sso:login")
def index(request):
    return render(request, "livequiz/index.html")

def createGame(request):
    return render(request, "livequiz/create.html")

def editGame(request, game_id):
    return render(request, "livequiz/edit.html")

def enterGame(request):
    return render(request, "livequiz/enter.html")

def playGame(request, game_id):
    return render(request, "livequiz/play.html")

