from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from .models import Game, GameSession, QuestionType1
from sso.models import User


@login_required(login_url="sso:login")
def index(request):
    return render(request, "livequiz/index.html", {
        "games": Game.objects.all(),
        "gamesessions": GameSession.objects.all(),
    })

def createGame(request):
    return render(request, "livequiz/create.html")

def editGame(request, game_code):
    return render(request, "livequiz/edit.html")

def enterGame(request):
    return render(request, "livequiz/enter.html")

def playGame(request, game_code):
    gamesession = GameSession.objects.get(code=game_code)
    game = gamesession.game
    print(game)
    
    
    return render(request, "livequiz/play.html", {
        "game": "aaa"
    })

""" action:
activate --> put
deactivate --> delete
retrieve --> get
"""

@csrf_exempt
def retrieveGame(request, game_code):
    print("RETRIEVE GAME API ROUTE")
    
    if request.method == "PARTY":
        return JsonResponse({"party": "HAHAHA"})
    
    gamesession = GameSession.objects.get(code=game_code)
    if request.method == "GET":
        print(gamesession)
        
        x = gamesession.game.get_questiontype1_order()
        print(x)
        print(x[0])
        print(x[1])
        print(x[2])
        print(type(x[1]))
        
        question = QuestionType1.objects.get(id=x[gamesession.current_question])
        print(question.question)        
        print(gamesession.current_question)
        
        question_ids = gamesession.game.get_questiontype1_order()
        curr_ques_no = gamesession.current_question
        question = QuestionType1.objects.get(id=question_ids[curr_ques_no - 1])
        return JsonResponse({
            "current_question": question.serialize(),
            "question_no": curr_ques_no,
        })


#x = serializers.serialize("json", gamesession)

