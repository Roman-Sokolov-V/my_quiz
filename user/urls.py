from django.urls import path
from user.views import register, current_user_page

app_name = "user"

urlpatterns = [
    path('', current_user_page, name='user_page'),
    path('register/', register, name='register'),

]
