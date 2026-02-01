from django.urls import path, include
from user.views import current_user_page, logout_link

app_name = "user"

urlpatterns = [
    path('current/', current_user_page, name='user_page'),
    path('', include('django.contrib.auth.urls')),
    path("logout-link/", logout_link, name="logout-link"),

]
