from django import forms
from django.contrib.auth.forms import UserCreationForm
from app.models import MyUser, Tickets


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


class SignUpForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'password1', 'password2', )


class AddTicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ['title', 'description']


class EditTicketForm(forms.ModelForm):
    class Meta:
        model = Tickets
        fields = ['title', 'description']
