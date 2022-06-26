from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password

from .models import User


def loginView(request):
    # attempt to sign user in and check if authentication successful
    if request.method == "POST":
        user = authenticate(request,
                            username = request.POST["username"],
                            password = request.POST["password"])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("livequiz:index"))
        else: return render(request, "sso/login.html", {
            "message": "Invalid username and/or password!"
        })
    else:
        # if user already logged in, redirects to dashboard
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("livequiz:index"))
        
        # if not render login form
        return render(request, "sso/login.html")


def logoutView(request):
    # logout the user, display successful logout message
    logout(request)
    return render(request, "sso/logout.html")


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        
        # username or email cannot be empty
        if not username or not email:
            return render(request, "sso/register.html", {
                "message": "Warning! Please fill all the required fields!",
                "username": username, "email": email,
            })
        
        # ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "sso/register.html", {
                "message": "Warning! Confirmation password does not match original password!",
                "username": username, "email": email,
            })
            
        # ensure password is not too simple
        try:
            validate_password(password)
        except ValidationError:
            return render(request, "sso/register.html", {
                "message": "Warning! Your password is too simple, pick another password!",
                "username": username, "email": email,
            })
            
        # ensure username is unique (not taken already)
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "sso/register.html", {
                "message": "Sorry, username already taken, please pick another username!",
                "username": username, "email": email,
            })
            
        # log user in and redirect to dashboard page
        login(request, user)
        return HttpResponseRedirect(reverse("livequiz:index"))
    else:
        # if user already logged in, redirects to dashboard
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("livequiz:index"))
        
        # if not render register form
        else: return render(request, "sso/register.html", {
            "username": "", "email": "",
        })
        

def comingsoonView(request):
    return render(request, "layout/comingsoon.html")
