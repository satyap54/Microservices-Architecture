from django.db import models

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=200)
    attendance = models.PositiveBigIntegerField(default=0)