from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from temple.models import God
from temple.forms import GodForm
from django.contrib import messages
import random

# Create your views here.


def index(request):

    context = { }

    return render(request, 'temple/index.html', context)


@login_required
def user_page(request):

    user = request.user
    gods = God.objects.all()

    follow_cap = 3 - request.user.userprofileinfo.gods_associated
    creation_cap = 3 - request.user.userprofileinfo.gods_created

    gods_sorted = []


    if request.method == "POST":

        if user.userprofileinfo.gods_associated < 1:

            for god in gods:
                gods_sorted.append([god.name, god.followers.count()])

            gods_sorted.sort(key=lambda tup: tup[1])
            print(gods_sorted)

            to_draw = []
            for god in gods_sorted:
                if god[1] == gods_sorted[0][1]:
                    to_draw.append(god[0])

            random.shuffle(to_draw)
            drawed_god=God.objects.filter(name=to_draw[0]).first()

            drawed_god.followers.add(user)
            user.userprofileinfo.gods_associated += 1

            drawed_god.save()
            user.userprofileinfo.save()

            return HttpResponseRedirect(reverse('userpage'))


    #If there is no POST. Display the Patron details.
    context = {
        'follow_cap': follow_cap,
        'creation_cap': creation_cap,
               }

    return render(request, 'temple/userpage.html', context)


@login_required
def panteon(request):

    user = request.user
    gods = God.objects.all()
    gods_cap = 3 - request.user.userprofileinfo.gods_associated

    gods_excluded = []

    context = {'gods': gods,
               'gods_cap': gods_cap,
               'gods_excluded': gods_excluded}

    for user_god in request.user.god_set.all():
        for god in gods:
            if god == user_god:
                gods_excluded.append(god.name)

    if request.method == "POST":
        god_name = request.POST.get("god_name")
        if user.userprofileinfo.gods_associated < 4:
            grabbed_god = God.objects.filter(name=god_name).first()

            grabbed_god.followers.add(user)
            user.userprofileinfo.gods_associated += 1

            grabbed_god.save()
            user.userprofileinfo.save()

            messages.success(request, f'Światło jest wszędzie.')
            return HttpResponseRedirect(reverse('userpage'))

    else:
        return render(request, 'temple/panteon.html', context)

@login_required
def create_god(request):
    if request.method == "POST":
        god_form = GodForm(data=request.POST)
        user = request.user

        if user.userprofileinfo.gods_created < 3:


            if god_form.is_valid():
                god = god_form.save()


                first_val = random.randint(1,10)
                second_val = 11-first_val
                third_val = random.randint(1,10)

                god.sacrum = first_val
                god.shaping = second_val
                god.vortex = third_val

                if 'profile_pic' in request.FILES:
                    god.profile_pic = request.FILES['profile_pic']

                user.userprofileinfo.gods_created += 1

                god.save()
                user.userprofileinfo.save()

                messages.success(request, f'Nowy bóg przybył do Panteonu')
                return HttpResponseRedirect(reverse('creategod'))
    else:
        gods_cap = 3 - request.user.userprofileinfo.gods_created
        god_form = GodForm
        context = {'god_form': god_form,
                   'gods_cap': gods_cap}

        return render(request, 'temple/creategod.html', context)

