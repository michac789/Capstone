from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "index.html")


def createGame(request):
    return HttpResponse("")

def editGame(request, game_id):
    return HttpResponse("")

def enterGame(request):
    return HttpResponse("")

def playGame(request, game_id):
    return HttpResponse("")

