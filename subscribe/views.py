from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from subscribe.forms import UserForm, UserProfileForm, UserProfileUpdate, UserUpdateForm
from django.http import HttpResponseRedirect
#Below is for login to work
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def user_register(request):
    # React on signal from interface - if user want to send data:
    if request.method == "POST":
        # Instantiate form variables
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            # Save basic user data to database
            user = user_form.save()
            # Hash the user's password
            user.set_password(user.password)
            # Save hashed password to database
            user.save()

            # Commit False is to prevent data of the profile_form to conflict with the user data
            profile = profile_form.save(commit=False)

            # Here you actually establish one-to-one relationship between the data of the user (already saved)
            # and the profile_form data. You define profile.user with the data gathered by user form.
            profile.user = user

            # Look for profile pic and save if found
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            print(user, "saved")

            messages.success(request, f'Udało się! Teraz może się zalogować.')
            return HttpResponseRedirect(reverse('login'))

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'subscribe/register.html', {'user_form': user_form,
                                                       'profile_form': profile_form,})


def user_login(request):
    """
    Handle the login mechanics.
    Grab data from the form if POST & login when validated.
    """

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                messages.error(request, f'Konto nieaktywne')
                return HttpResponseRedirect(reverse('login'))
        else:
            print('***')
            print('Ktoś chciał się zalogować i mu nie wyszło')
            print(f'Username: {username}; Password: {password}')

            messages.error(request, f'Niepoprawne logowanie')
            return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'subscribe/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, f'Użytkownik wylogowany')
    return HttpResponseRedirect(reverse('index'))


@login_required
def profile_update(request):
    if request.method == 'POST':
        update_user_form = UserUpdateForm(request.POST,
                                          instance=request.user)
        update_picture_form = UserProfileUpdate(request.POST,
                                                request.FILES,
                                                instance=request.user.userprofileinfo)

        if update_user_form.is_valid() and update_picture_form.is_valid():
            update_user_form.save()
            update_picture_form.save()
            messages.success(request, f'Twoje konto zostało aktualizowane.')
            return HttpResponseRedirect(reverse('userpage'))


    else:
        update_user_form = UserUpdateForm(instance=request.user)
        update_picture_form = UserProfileUpdate(instance=request.user.userprofileinfo)

    context = {
        'up_pic_form': update_picture_form,
        'up_user_form': update_user_form,
    }

    return render(request, 'subscribe/profileupdate.html', context)