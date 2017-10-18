import json

from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage, send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from accounts.models import Profile
from accounts.token import account_activation_token
from myproject import settings
from .forms import SignUpForm, EditProfileForm, ChangeProfilePhoto


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = False
            user.save()
            # auth_login(request, user)
            # return redirect('home') # после этих двух строк начинается подтверждения мыла
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            send_mail(mail_subject, message, settings.EMAIL_HOST_USER, [to_email])
            # email.send()
            return HttpResponse('Activate your account.')

    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_profile = Profile.objects.filter() # название переменной ебаное! эта строчка значит, что фильтруем объекты таблицы профиль без параметров фильтра
    user_rating = Profile.objects.filter(profile_rating=user.profile.profile_rating)
    rating = []
    if request.is_ajax():
        # если данные с формы up то +1 иначе -1
        if request.POST.get('action') == 'up':
            user.profile.profile_rating += 1
            user.save()
            rating.append(user.profile.profile_rating)
            return HttpResponse(json.dumps(rating))
        else:
            user.profile.profile_rating -= 1
            user.save()
            rating.append(user.profile.profile_rating)
            return HttpResponse(json.dumps(rating))

    return render(request, 'profile.html', {'user': user, 'user_profile': user_profile})



def edit_profile(request):
    user = request.user
    form = EditProfileForm(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            user.first_name = request.POST.get('first_name')
            user.last_name = request.POST.get('last_name')
            user.save()

            return redirect(to='profile/{}'.format(user))

    context = {
        "form": form
    }

    return render(request, "edit_profile.html", context)


def edit_profile_photo(request):
    user = request.user
    form = ChangeProfilePhoto(request.POST, request.FILES)
    if request.method == 'POST':
        if form.is_valid():
            user.profile.profile_img.save(user.username, request.FILES["profile_img"])
            return redirect(to='profile/{}'.format(user))

    context = {
        "form": form
    }

    return render(request, "edit_profile.html", context)
