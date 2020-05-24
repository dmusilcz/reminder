from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class LoginForm(AuthenticationForm):
    remember_me = forms.BooleanField(required=False, label='Keep me logged in', widget=forms.CheckboxInput())


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserInformationUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', )