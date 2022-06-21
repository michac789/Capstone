from django.urls import path
from . import views

app_name = "sso"
urlpatterns = [
    path("login", views.loginView, name="login"),
    path("logout", views.logoutView, name="logout"),
    path("register", views.register, name="register"),
]
