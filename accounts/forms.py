from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from accounts.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.CharField(max_length=254, required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class EditProfileForm(forms.ModelForm):
    # username = forms.CharField(max_length=50)
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')
    #profile_img = forms.ImageField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name']


class ChangeProfilePhoto(forms.ModelForm):
    profile_img = forms.ImageField()

    class Meta:
        model = Profile
        fields = ['profile_img']
