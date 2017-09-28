from django.contrib.auth import login as auth_login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import SignUpForm, EditProfileForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def profile(request):
    return render(request, 'profile.html')

def edit_profile(request):

    user = request.user
    form = EditProfileForm(request.POST or None, initial={'username': user.username, 'first_name': user.first_name, 'last_name': user.last_name})
    if request.method == 'POST':
        if form.is_valid():
            user.username = request.POST['username']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']

            user.save()
            return redirect(to=profile)

    context = {
        "form": form
    }

    return render(request, "edit_profile.html", context)