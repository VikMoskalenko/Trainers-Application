from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
class Trainer_description(models.Model):
    text = models.TextField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

class Trainer_Schedule(models.Model):
    datetime_start = models.DateField()
    datetime_end = models.DateField()
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)

class Services(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    trainer = models.ForeignKey(User, on_delete=models.CASCADE)
    price = models.FloatField()
    duration = models.IntegerField()
    level = models.IntegerField()