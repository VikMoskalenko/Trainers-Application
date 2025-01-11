from django.urls import path

from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.trainer_registration, name='trainer_registration'),
    # path("<category_id>", views.category_page, name="category_page"),
    path("<trainer_id>", views.trainer_page, name="trainer_page"),
   # path("<service_id>", views.trainer_service, name="trainer_service"),
    path("<trainer_id>/<service_id>/booking", views.booking_for_user, name="booking_for_user"),
   # path("service/", views.service_page, name="service_page"),
    path("<trainer_id>/service/<service_id>/", views.trainer_service, name="trainer_service"),
    path("<trainer_id>/service/", views.service_page, name="service_page"),



]