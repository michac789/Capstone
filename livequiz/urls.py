from django.urls import path
from . import views

app_name = "livequiz"
urlpatterns = [
    path("dashboard", views.index, name="index"),
    path("create", views.createGame, name="create"),
    path("create/<int:game_code>", views.editGame, name="edit"),
    path("play/entercode", views.enterGame, name="entercode"),
    path("play/<str:game_code>", views.playGame, name="play"),
    
    # API route
    path("api/retrieve/<str:game_code>", views.retrieveGame),
]
