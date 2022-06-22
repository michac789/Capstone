from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from json import loads

from .models import Game, GameSession, QuestionType1, AnswerPairType1
from sso.models import User
from .forms import GameForm, CodeForm, QuestionForm


@login_required(login_url="sso:login")
def index(request):
    return render(request, "livequiz/index.html", {
        "games": Game.objects.all(),
        "gamesessions": GameSession.objects.all(),
    })


@login_required(login_url="sso:login")
def createGame(request):
    if request.method == "POST":
        form = GameForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            newgame = Game(creator = request.user, title = title, description = description)
            newgame.save()
            return HttpResponseRedirect(reverse("livequiz:edit", kwargs = {
                "game_id": newgame.id,
            }))
        else:
            return render(request, "livequiz/create.html", { "form": form,})
    return render(request, "livequiz/create.html", { "form": GameForm,})


@login_required(login_url="sso:login")
def editGame(request, game_id): # TODO - buggy
    game = Game.objects.get(id = game_id)
    return render(request, "livequiz/edit.html", {
        "game": game,
        "questions": game.questions,
    })


@login_required(login_url="sso:login")
def enterGame(request):
    if request.method == "POST":
        form = CodeForm(request.POST)
        valid_codes = GameSession.objects.all().values_list('code', flat = True)
        if form.is_valid() and form.cleaned_data["sessioncode"] in valid_codes:
            return HttpResponseRedirect(reverse("livequiz:play", kwargs = {
                "game_code": form.cleaned_data["sessioncode"],
            }))
        else:
            return render(request, "livequiz/enter.html", {
                "form": form,
                "error": "invalid code!"
            })
    return render(request, "livequiz/enter.html", { "form": CodeForm,})


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


def saveQuestion(request, ques_id):
    print("SAVE GAME API ROUTE")
    
    # check if correct answer is valid (can only be 1-4)
    data = loads(request.body)
    if data["ans"] not in [1, 2, 3, 4]:
        return JsonResponse({
            "error": "invalid answer option"
        }, status = 400)
        
    # 'POST' method: create new question and associate with current game
    if request.method == "POST":
        pass # TODO

    # check if question id is valid
    try: q = QuestionType1.objects.get(id=ques_id)
    except QuestionType1.DoesNotExist:
        return JsonResponse({
            "error": "invalid question id"
        }, status = 400)
        
    # check if user is valid (must be the creator of the game)
    if request.user != q.game_origin.creator:
        return JsonResponse({
            "error": "unauthorized user"
        }, status = 401)
    
    # 'PUT' method: update existing question with new values
    if request.method == "PUT":
        q.saveedit({"ques":data["ques"], "opt1":data["opt1"], "opt2":data["opt2"],
                   "opt3":data["opt3"], "opt4":data["opt4"], "ans":data["ans"],})
        return JsonResponse({
            "success": "edit succesful",
            "q": data,
        })
        
    # return error for other request method
    else: return JsonResponse({
            "error": "invalid request method, only accepting PUT & POST method"
        }, status = 404)



