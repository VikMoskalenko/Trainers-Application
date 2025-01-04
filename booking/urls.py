from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_page, name="booking_page"),
    path("cancel/", views.booking_cancel, name="booking_cancel"),
    path("acception/", views.booking_acception, name="booking_acception"),
]