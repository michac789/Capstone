from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.core import serializers
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from json import loads

from .models import Game, GameSession, QuestionType1, AnswerPairType1
from sso.models import User
from .forms import GameForm, CodeForm, AddQuesForm


@login_required(login_url="sso:login")
def index(request):
    # 'POST' method: delete gamesession (valid as long as gamesession exist & user must be the creator)
    if request.method == "POST":
        session_id = request.POST["session_id"]
        try:
            gamesession = GameSession.objects.get(id = session_id)
        except GameSession.DoesNotExist:
            raise Http404("Gamesession not found!")
        if request.user != gamesession.host:
            return HttpResponse("Unauthorized user!", status = 401)
        gamesession.delete()
    
    # render dashboard page
    return render(request, "livequiz/index.html", {
        "games": Game.objects.all(),
        "gamesessions": GameSession.objects.all(),
    })


@login_required(login_url="sso:login")
def createGame(request):
    # 'POST' method: handles form submission of new game creation, redirect to edit page
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
        else: return render(request, "livequiz/create.html", { "form": form,})
        
    # 'GET' method: render html with empty form
    return render(request, "livequiz/create.html", { "form": GameForm,})


@login_required(login_url="sso:login")
def editGame(request, game_id):
    # make sure game_id is valid
    try: game = Game.objects.get(id = game_id)
    except KeyError:
        return HttpResponseBadRequest("Bad request: missing game id!")
    except Game.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: invalid game id!")
    
    # 'POST' method: handles form submission for number of new questions in this game, then refresh page
    if request.method == "POST":
        form = AddQuesForm(request.POST)
        if form.is_valid():
            ques_count = form.cleaned_data["ques_count"]
            for _ in range(int(ques_count)):
                QuestionType1(game_origin = game, answer = 1).save()
            return HttpResponseRedirect(reverse("livequiz:edit", args = (game_id,)))
        else:
            return render(request, "livequiz/edit.html", {
                "game": game, "questions": game.questions, "form": form,
            })
            
    # 'GET' method: render edit page with questions and form to add more question
    return render(request, "livequiz/edit.html", {
        "game": game, "questions": game.questions, "form": AddQuesForm,
    })


@login_required(login_url="sso:login")
def hostGame(request):
    # 'POST' method: creates new game session if game_id is an integer and valid, redirect to play page
    if request.method == "POST":
        try: game_id = int(request.POST["game_id"])
        except TypeError: return render(request, "livequiz/host.html", {
                "message": "Game ID must be an integer!"
            })
        game_id = int(request.POST["game_id"])
        if game_id not in list(Game.objects.all().values_list('id', flat = True)):
            return render(request, "livequiz/host.html", {
                "message": "Invalid Game ID!",
            })
        game_session = GameSession.objects.create(host = request.user,
                                   game = Game.objects.get(id = game_id))
        return HttpResponseRedirect(reverse("livequiz:play", kwargs = {
            "game_code": game_session.code,
        }))

    # 'GET' method: renders the host html page
    return render(request, "livequiz/host.html")


@login_required(login_url="sso:login")
def enterGame(request):
    # 'POST' method: handles form submission, if valid redirect to play page as participants
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
            
    # 'GET' method: renders enter code html page and form
    return render(request, "livequiz/enter.html", { "form": CodeForm,})


@login_required(login_url="sso:login")
def playGame(request, game_code):
    # make sure game_code is valid
    try: gamesession = GameSession.objects.get(code=game_code)
    except KeyError:
        return HttpResponseBadRequest("Bad request: missing game session code!")
    except GameSession.DoesNotExist:
        return HttpResponseBadRequest("Bad Request: invalid game session code!")
    
    # render play page (interaction & functionality made through js and api routes)
    gamesession = GameSession.objects.get(code=game_code)
    return render(request, "livequiz/play.html", {
        "game": gamesession.game,
        "active": gamesession.active,
        "gamesession": gamesession,
        "admin": request.user == gamesession.host,
    })


@csrf_exempt
def retrieveGame(request, game_code):
    print("RETRIEVE GAME API ROUTE")
    
    # check if gamesession is valid
    try: gamesession = GameSession.objects.get(code = game_code)
    except GameSession.DoesNotExist:
        return JsonResponse({
            "error": "invalid gamesession"
        }, status = 400)

    # return jsonresponse of current question and its options
    if request.method == "VIEW":
        question_ids = gamesession.game.get_questiontype1_order()
        curr_ques_no = gamesession.current_question
        question = QuestionType1.objects.get(id=question_ids[curr_ques_no - 1])
        return JsonResponse({
            "current_question": question.serialize(),
            "question_no": curr_ques_no,
        })
    
    # return jsonresponse of current game state (started or not)
    elif request.method == "GET":
        return JsonResponse({ "status": gamesession.status(),})
    
    # if gamesession is not closed yet, register user's answer
    elif request.method == "POST": # TODO - maybe change to 'PUT' method instead??
        if gamesession.status() == "closed" or gamesession.status() == "prep":
            return JsonResponse({ "message": "closed",})
        # create new answerpair & save to database
        data = loads(request.body)
        a = data["answer"]
        question_ids = gamesession.game.get_questiontype1_order()
        curr_ques_no = gamesession.current_question
        q = QuestionType1.objects.get(id=question_ids[curr_ques_no - 1])
        ans = AnswerPairType1(player=request.user, answer=a, question=q, gamesession=gamesession)
        ans.save()
        # return successful jsonresponse
        return JsonResponse({
            "message": "submitted",
            "answer": a,
        })
        
    # TODO - if game not started, add error checking to view as question = 0 result in error
    # TODO - only able to register answer once for each user, cannot register anymore if already there
    # TODO - do something if game is over
    # TODO - tally? display score?


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
        }, status = 401)
    
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
        return JsonResponse({ "message": "next question",})
    #TODO - check if question still exist, if end of question then do ???
    
    elif request.method == "RESET": pass # TODO under consideration ???
    
    # return error for other request method
    else: return JsonResponse({
            "error": "invalid request method, only accepting START, CLOSE, NEXT"
        }, status = 400)


def saveQuestion(request, ques_id):
    print("SAVE EDITED QUESTION API ROUTE")

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
        
    # 'DELETE' method: delete a particular question
    if request.method == "DELETE":
        q.delete()
        return JsonResponse({
            "success": "question deleted",
        })
    
    # check if correct answer input is valid (can only be 1-4)
    data = loads(request.body)
    if data["ans"] not in [1, 2, 3, 4]:
        return JsonResponse({
            "error": "invalid answer option"
        }, status = 400)
    
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
            "error": "invalid request method, only accepting PUT and DELETE method"
        }, status = 404)
