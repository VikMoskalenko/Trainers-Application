from dateutil import parser
import datetime, timedelta
from django.contrib.auth.models import User, Group
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
#from datetime import timedelta
from trainer import models
from trainer.utils import booking_time
import trainer.models
import booking.models as booking_models
from users.models import User as CustomUser
from users.forms import registerForm
from trainer.models import Services
from django.utils import timezone
# Create your views here.
def homepage(request):
    return render(request, 'homepage.html')

def category_page(request):
    return HttpResponse("<h1>Welcome to my category page</h1>")
def trainer_page(request, trainer_id):

    if request.user.groups.filter(name="Trainer").exists():
        if request.method == 'GET':
            service_categories = trainer.models.Category.objects.all()
            my_services = trainer.models.Services.objects.filter(trainer=request.user).all()
            return render(request, "trainer.html", {
                "categories": service_categories, "services": my_services
            })
    else:
        trainer_model = User.objects.get(pk=trainer_id)
        trainer_data = trainer.models.Trainer_description.objects.filter(trainer=trainer_model)
        trainer_schedule = trainer.models.Trainer_Schedule.objects.filter(trainer=trainer_model)
        return render(request, "account.html", {
            "trainer_data": trainer_data, "trainer_schedule": trainer_schedule
        })

def trainer_service(request, trainer_id, service_id):
    current_trainer = User.objects.get(pk=trainer_id)
    specific_service = models.Services.objects.get(pk=service_id)

    if request.method == 'GET':
        today =  timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        i = 1
        available_times = []

        while i <= 7:
            cur_date = today + datetime.timedelta(days=i)
            training_bookings = booking_models.Booking.objects.filter(
                trainer=current_trainer,
                datetime_start=cur_date.date()
                #datetime_start__date=cur_date.date()
            ).all()
            booking_list = [(itm.datetime_start, itm.datetime_end) for itm in training_bookings]
            training_schedule = trainer.models.Trainer_Schedule.objects.filter(
                trainer=current_trainer,
                datetime_start=cur_date.date()
                #datetime_start__date=cur_date.date()
            ).values('datetime_start', 'datetime_end')
            available_times += trainer.utils.booking_time(training_schedule, training_bookings, cur_date)
            i += 1
        return render(request, 'trainer_service_page.html', {
            'specific_service': specific_service, 'available_times': available_times
        })

    else:
        booking_start = parser.parse(request.POST.get('booking_start'))
        current_user = User.objects.get(id=request.user.id)
        booking_models.Booking.objects.create(
            trainer=current_trainer,
            user=current_user,
            service=specific_service,
            datetime_start=booking_start,
            datetime_end=booking_start + datetime.timedelta(minutes=specific_service.duration)
        )
        #return redirect("trainer_service", trainer_id=trainer_id, service_id=service_id)
        return render(request, "trainer_service_page.html")

def service_page(request):
    if request.method == 'GET':
        services = Services.objects.all()
        return render(request, "trainer_service_page.html", context={"services": services})
    else:
        if request.user.groups.filter(name="Trainer").exists():
            form_data = request.POST
            service_cat = trainer.models.Category.objects.get(pk=form_data['category'])
            service = trainer.models.Services(
                level=form_data['level'],
                duration=form_data['duration'],
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
        trainer_signup = registerForm()
        return render(request, 'trainer_signup.html', {'trainer_signup': trainer_signup})
    else:
        trainer_signup = registerForm(request.POST)
        if trainer_signup.is_valid():
            trainer_group = Group.objects.get(name="Trainer")
            created_user = trainer_signup.save()
            created_user.groups.add(trainer_group)
            return redirect('user_login')
        else:
            print(trainer_signup.errors)  # Debugging line
            return render(request, 'trainer_signup.html', {'trainer_signup': trainer_signup})

    # if request.method == 'GET':
    #     trainer_signup = registerForm()
    #
    #     return render(request, 'trainer_signup.html', {'trainer_signup': trainer_signup})
    # else:
    #     trainer_signup = registerForm(request.POST)
    #     if trainer_signup.is_valid():
    #
    #         trainer_group = Group.objects.get(name="Trainer")
    #         created_user = trainer_signup.save()
    #         created_user.groups.add(trainer_group)
    #         trainer_signup.save()
    #
    #     # username = request.POST.get('username')
    #     # password = request.POST.get('password')
    #     # email = request.POST.get('email')
    #     # firstname = request.POST.get('firstname')
    #     # lastname = request.POST.get('lastname')
    #
    #    # user = User.objects.create_user(username, email, password, firstname=firstname, lastname=lastname)
    #    # user.groups.add(1)
    #     #get trainer group
    #
    #     # user.groups.add(trainer_group)
    #     # user.save()
    #     return HttpResponse(request, 'login.html')

