from django.contrib.auth import get_user_model
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views import generic

from user.forms import UserRegisterForm


# Create your views here.


def current_user_page(request: HttpRequest) -> HttpResponse:
    user = request.user
    if user.is_authenticated:
        context = {"current_user": user}
        return render(request, template_name='user/about_user.html', context=context)


@login_required
def logout_link(request):
    return render(request, "registration/logout_link.html")


class RegisterView(generic.CreateView):
    model = get_user_model()
    form_class = UserRegisterForm
    success_url = reverse_lazy("home-page")
