from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect

import trainer.models
#from django.contrib.auth.models import Group


# Create your views here.
def category_page(request):
    return HttpResponse("<h1>Welcome to my category page</h1>")


def trainer_page(request, trainer_id):
    if request.user.groups.filter(name="Trainer").exists():
         if request.method == 'GET':
            service_categories = trainer.models.Category.objects.all()
            my_services = trainer.models.Service.objects.filter(trainer = request.user).all()
         return render(request,"trainer.html", {"categories": service_categories, "services": my_services}) #form with adding service

         return HttpResponse("<h1>Welcome to my trainer page</h1>")
    else:
        trainer_model = User.objects.get(pk=trainer_id)
        trainer_data = trainer.models.Trainer_description.objects.filter(trainer=trainer_model)
        trainer_schedule = trainer.models.Trainer_Schedule.objects.filter(trainer=trainer_model)
        return render(request, "account.html", context={"trainer_data": trainer_data, "trainer_schedule": trainer_schedule})

def trainer_service_page(request, user_id, service_id):
    return HttpResponse("<h1>Welcome to my trainer service page</h1>")

def service_page(request):
    if request.method == 'GET':
        services = trainer.Service.objects.all()
        return render(request, "services.html", context={"services": services})
    else:
        if request.user.groups.filter(name="Trainer").exists():
             form_data = request.POST
             service_cat = trainer.models.Category.objects.get(pk=form_data['category'])
             service = trainer.models.Service(
                 level=form_data['level'],
                 duration =form_data['duration'],
                 price=form_data['price'],
                 category=service_cat,
                 trainer=request.user
             )
             service.save()
             return redirect("/trainer/")
        else:
            raise HttpResponseForbidden()


def booking_for_user(request):
    return HttpResponse("<h1>Welcome to my booking page</h1>")

def trainer_registration(request):
    if request.method == 'GET':
        return render(request, 'trainer_signup.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')

        user = User.objects.create_user(username, email, password, firstname=firstname, lastname=lastname)
       # user.groups.add(1)
        #get trainer group
        trainer_group = Group.objects.get(name="Trainer")
        user.groups.add(trainer_group)
        user.save()
        return HttpResponse("Hello, world. You're at the polls index.")

