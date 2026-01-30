from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def register(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Page for user registration')

def current_user_page(request: HttpRequest) -> HttpResponse:
    user = request.user
    if user.is_authenticated:
        context = {"current_user": user}
    return render(request, template_name='user/about_user.html', context=context)

def login(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Login page')

def logout(request: HttpRequest) -> HttpResponse:
    return HttpResponse('Logout page')