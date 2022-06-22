from django.urls import path
from . import views

app_name = "livequiz"
urlpatterns = [
    # Regular URL routes
    path("dashboard", views.index, name="index"),
    path("create", views.createGame, name="create"),
    path("create/<int:game_id>", views.editGame, name="edit"),
    path("create/host", views.hostGame, name="host"),
    path("play/entercode", views.enterGame, name="entercode"),
    path("play/<str:game_code>", views.playGame, name="play"),
    
    # API routes
    path("api/retrieve/<str:game_code>", views.retrieveGame),
    path("api/action/<str:game_code>", views.gameAction),
    path("api/savequestion/<str:ques_id>", views.saveQuestion),
]
