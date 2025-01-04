from django.http import HttpResponse
from django.shortcuts import render

import trainer


# Create your views here.
def category_page(request):
    return HttpResponse("<h1>Welcome to my category page</h1>")

def trainer_page(request, trainer_id):
    if request.method == 'GET':
        service_categories = trainer.models.Category.objects.all()
        my_services = trainer.models.Service.objects.filter(trainer = request.user).all()
        return render(request,"trainer.html", {"categories": service_categories, "services": my_services}) #form with adding service

    return HttpResponse("<h1>Welcome to my trainer page</h1>")

def trainer_service_page(request, user_id, service_id):
    return HttpResponse("<h1>Welcome to my trainer service page</h1>")

def service_page(request):
    if request.method == 'POST':
        form_data = request.POST
        service_cat = trainer.models.Category.objects.get(pk=form_data['category'])

        service = trainer.models.Service(
            level=form_data['level'],
            duration =form_data['duration'],
            price=form_data['price'],
            category=service_cat,
            trainer=request.user,
        )
        service.save()
    return HttpResponse("<h1>Welcome to my service page</h1>")

def booking_for_user(request):
    return HttpResponse("<h1>Welcome to my booking page</h1>")

