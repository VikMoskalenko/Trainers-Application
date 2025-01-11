from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from users import forms

# Create your views here.

def user_page(request):
    form_login = forms.loginForm()
    return render(request, 'account.html', context={'form_login': form_login})
    #return HttpResponse("Hello, world. You're at the polls index.")

def specific_user(request, user_id):
    return HttpResponse("Hello, world. You're at the polls index.")

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
            # Optionally, assign groups
            client_group = Group.objects.get(name="Client")
            new_user.groups.add(client_group)
            return render(request, 'login.html')

    else:
        register_form = forms.registerForm()
    return render(request, 'register.html', {'register_form': register_form})
