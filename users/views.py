from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from pyexpat.errors import messages

from users import forms
from users.forms import UpdateProfileForm


# Create your views here.

def user_page(request):
    form_login = forms.loginForm()
    return render(request, 'account.html', context={'form_login': form_login})
    #return HttpResponse("Hello, world. You're at the polls index.")

def specific_user(request, user_id):
    if request.user.is_authenticated:
        if request.method == 'GET':
            user_profile = get_object_or_404(User, id=user_id)
            #current_user = User.objects.get(id=user_id)
            update_form = UpdateProfileForm(initial={'first_name': user_profile.first_name,
                                                     'last_name': user_profile.last_name,
                                                     'email': user_profile.email,})
            group_list =[]
            for group in request.user.groups.all():
                group_list.append(group.name)
            context = {
                'user_profile': user_profile,
                'group_list': group_list,
                 'update_form': update_form,
            }
            return render(request, 'profile.html')
    elif request.method == 'POST':
        update_form = UpdateProfileForm(request.POST)
        if update_form.is_valid():
            User.objects.filter(id=user_id).update(**update_form.cleaned_data)
        messages.success(request, f'Your account has been edited successfully!')
        return redirect(f'/user/{user_id}')
    else:
        return render(request, 'homepage.html', context={'is_authenticated': False} )

def login_page(request):
    if request.method == 'GET':
        form_login = forms.loginForm()
        return render(request, 'login.html', context = {'form_login': form_login})
    else:
        form_login = forms.loginForm(request.POST)
        # username = request.POST.get('username')
        # password = request.POST.get('password')
        if form_login.is_valid():
            username = form_login.cleaned_data['username']
            password = form_login.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, 'account.html')

        return render(request, 'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("You are now logged out.")
    return HttpResponse("You need to be logged in first.")

def register(request):
    if request.method == 'POST':
        register_form = forms.registerForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save()
            # Optionally, assign group
            client_group = Group.objects.get(name="Client")
            new_user.groups.add(client_group)
            return render(request, 'login.html')

    else:
        register_form = forms.registerForm()
    return render(request, 'register.html', {'register_form': register_form})
