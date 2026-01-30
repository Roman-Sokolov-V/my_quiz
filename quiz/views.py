from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from user.models import User

def home_page(request: HttpRequest) -> HttpResponse:
    context = {
        "users": User.objects.count(),
        "topics": 40,                  #  todo
        "quizzes": 200                 #  todo
    }

    return render(request, "home.html", context=context)