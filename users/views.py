from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def user_page(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def specific_user(request, user_id):
    return HttpResponse("Hello, world. You're at the polls index.")

def login_page(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("You are now logged in.")
        else:
            return render(request, 'login.html')

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponse("You are now logged out.")
    return HttpResponse("You need to be logged in first.")

def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        user = User.objects.create_user(username, email, password, firstname=firstname, lastname=lastname)


       # user.groups.add(1)

        #get trainer group
        client_group = Group.objects.get(name="Client")
        user.groups.add(client_group)
        user.save()
        return HttpResponse("Hello, world. You're at the polls index.")