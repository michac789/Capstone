from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from json import loads

from .models import Game, GameSession, QuestionType1, AnswerPairType1
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
        "game": game,
        "active": gamesession.active,
        "gamesession": gamesession,
    })

""" action:
activate --> put
deactivate --> delete
retrieve --> get
checkstarted --> view


"""
@csrf_exempt
def retrieveGame(request, game_code):
    print("RETRIEVE GAME API ROUTE")
    
    # check if gamesession is valid
    try: gamesession = GameSession.objects.get(code=game_code)
    except GameSession.DoesNotExist:
        return JsonResponse({
            "error": "invalid gamesession"
        }, status = 400)

    # 
    if request.method == "VIEW":
        # temp = gamesession.game.get_questiontype1_order()
        # print(x)
        # print(x[0])
        # print(x[1])
        # print(x[2])
        # print(type(x[1]))
        
        # question = QuestionType1.objects.get(id=temp[gamesession.current_question])
        # print(question.question)        
        # print(gamesession.current_question)
        # print(gamesession.serialize())
        
        question_ids = gamesession.game.get_questiontype1_order()
        curr_ques_no = gamesession.current_question
        question = QuestionType1.objects.get(id=question_ids[curr_ques_no - 1])
        return JsonResponse({
            "current_question": question.serialize(),
            "question_no": curr_ques_no,
            "open": gamesession.stillopen,
        })
        
    elif request.method == "GET":
        print(gamesession.serialize())
        return JsonResponse({
            "started": gamesession.active,
        })
        
    elif request.method == "POST":
        data = loads(request.body)
        a = data["answer"]
        
        question_ids = gamesession.game.get_questiontype1_order()
        curr_ques_no = gamesession.current_question
        q = QuestionType1.objects.get(id=question_ids[curr_ques_no - 1])
        
        ans = AnswerPairType1(player=request.user, answer=a, question=q, gamesession=gamesession)
        ans.save()
        
        return JsonResponse({
            "message": "submitted",
            "answer": a,
        })

#x = serializers.serialize("json", gamesession)



@csrf_exempt
@login_required(login_url="sso:login")
def gameAction(request, game_code):
    print("GAMEACTION API ROUTE")
    
    # check if gamesession is valid
    try: gamesession = GameSession.objects.get(code=game_code)
    except GameSession.DoesNotExist:
        return JsonResponse({
            "error": "invalid gamesession"
        }, status = 400)
        
    # check if user is valid (the host of the gamesession)
    if request.user != gamesession.host:
        return JsonResponse({
            "error": "unauthorized user"
        }, status = 400)
    
    # 'START' method: activate the game
    if request.method == "START":
        gamesession.activate()
        return JsonResponse({ "message": "game started",})
    
    # 'CLOSE' method: close current question (cannot be answered anymore)
    elif request.method == "CLOSE":
        gamesession.closequestion()
        return JsonResponse({ "message": "question closed",})
        
    # 'NEXT' method: go to the next question
    elif request.method == "NEXT":
        gamesession.nextquestion()
        return JsonResponse({ "message": "next question",}) #TODO - check if question still exist
    
    elif request.method == "RESET": pass
    
    # return error for other request method
    else: return JsonResponse({
            "error": "invalid request method, only accepting START, CLOSE, NEXT"
        }, status = 400)



