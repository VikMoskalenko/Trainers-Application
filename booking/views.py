from django.http import HttpResponse
from django.shortcuts import render


def booking_page(request):
    return HttpResponse("This is the booking page.")

def booking_cancel(request):
    return HttpResponse("Booking cancellation successful.")

def booking_acception(request):
    return HttpResponse("Booking acceptance successful.")