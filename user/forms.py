from django.contrib.auth import get_user_model
from django.contrib.auth.forms import BaseUserCreationForm
from django import forms


class UserRegisterForm(BaseUserCreationForm):
    is_author = forms.BooleanField(required=False, label="I want to register as an author")
    class Meta:
        model = get_user_model()
        fields = ('email', 'is_author')