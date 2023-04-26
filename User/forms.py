from django import forms
from django.contrib.auth.forms import UserCreationForm
from User.models import User


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email Address')

    class Meta(UserCreationForm):
        model = User
        fields = UserCreationForm.Meta.fields + ("email",)
