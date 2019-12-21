from django.shortcuts import render
from django.urls import reverse
from subscribe.forms import UserForm, UserProfileForm
from django.http import HttpResponseRedirect, HttpResponse
#Below is for login to work
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


# Create your views here.


def index(request):
    return render(request, 'subscribe/index.html')


def user_register(request):
    # React on signal from interface - if user want to send data:
    if request.method == "POST":
        # Instantiate form variables
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # Validate input with pre-built validation
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

            # Login the user
            login(request, user)
            # And direct to personal userpage
            return HttpResponseRedirect(reverse('userpage'))

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
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('userpage'))
            else:
                return HttpResponse('Konto nieaktywne')
        else:
            print('***')
            print('Ktoś chciał się zalogować i mu nie wyszło')
            print(f'Username: {username}; Password: {password}')

            return HttpResponse('Niepoprawne logowanie')
    else:
        return render(request, 'subscribe/login.html')


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def user_page(request):
    return render(request, 'subscribe/userpage.html')
