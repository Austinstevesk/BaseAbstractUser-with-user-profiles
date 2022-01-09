from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import fields
from .models import User, Profile

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone')

class ProfileUpdateForm (forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'