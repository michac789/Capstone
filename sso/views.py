from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from .models import User


def loginView(request):
    if request.method == "POST":
        user = authenticate(request,
                            username = request.POST["username"],
                            password = request.POST["password"])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("livequiz:index"))
        return render(request, "sso/login.html", {
            "message": "invalid"
        })
    return render(request, "sso/login.html")


def logoutView(request):
    logout(request)
    return HttpResponseRedirect(reverse("livequiz:index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sso/register.html", {
                "message": "Passwords must match.",
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sso/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("livequiz:index"))
    else:
        return render(request, "sso/register.html")
