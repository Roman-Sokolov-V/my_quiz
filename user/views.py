from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.


def current_user_page(request: HttpRequest) -> HttpResponse:
    user = request.user
    if user.is_authenticated:
        context = {"current_user": user}
        return render(request, template_name='user/about_user.html', context=context)


@login_required
def logout_link(request):
    return render(request, "registration/logout_link.html")