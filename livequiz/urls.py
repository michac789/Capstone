from django.urls import path
from . import views

app_name = "livequiz"
urlpatterns = [
    path("dashboard", views.index, name="index"),
    path("create", views.createGame, name="create"),
    path("create/<int:game_id>", views.editGame, name="edit"),
    path("play/entercode", views.enterGame, name="entercode"),
    path("play/<int:game_id>", views.playGame, name="play"),
]
