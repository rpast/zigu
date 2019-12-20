from django.shortcuts import render, HttpResponse
from subscribe.models import User, UserProfileInfo
from subscribe.forms import UserForm, UserProfileForm

# Create your views here.


def index(request):
    return render(request, 'subscribe/index.html')


def user_register(request):
    # Monitor the state of user
    registered = False

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
            profile = profile_form.save(commit= False)

            # Here you actually establish one-to-one relationship between the data of the user (already saved)
            # and the profile_form data. You define profile.user with the data gathered by user form.
            profile.user = user

            profile.save()

            # add saving the profile pic

            print(user_form.cleaned_data, profile_form.cleaned_data)

            registered = True

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'subscribe/register.html', {'user_form': user_form,
                                                           'profile_form': profile_form,
                                                           'registered': registered})


def user_login(request):
    return HttpResponse('tutaj będzie strona logowania')


def user_logout(request):
    return HttpResponse('tutaj się wylogujesz')


def user_page(request):
    return HttpResponse('tutaj będzie spersonalizowana strona użytkownika')
