from django.utils.timezone import now

from django.contrib.auth.models import User
from django.db import models
from trainer.models import Services


# Create your models here.
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    trainer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainer')
    datetime_start = models.DateTimeField()
    datetime_end = models.DateTimeField(default=now)
    service  = models.ForeignKey(Services, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)