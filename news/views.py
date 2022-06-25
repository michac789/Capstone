from django.shortcuts import render

from .models import Information


def index(request):
    return render(request, "news/index.html", {
        "infos": Information.objects.all(),
        "admin": (False if request.user.is_anonymous else
                  request.user.status in ["T1", "T2"]),
        "active": "news",
    })


def renderPage(request, id):
    print(Information.objects.get(id = id).serialize())
    return render(request, "news/page.html", {
        "md": Information.objects.get(id = id).serialize(),
        "admin": (False if request.user.is_anonymous else
                  request.user.status in ["T1", "T2"]),
        "active": "news",
    })
