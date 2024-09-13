from django.db import models

# Create your models here.
class user_registration_model(models.Model):
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)

class professional_registration_model(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    drone_type = models.CharField(max_length=255)
    load_capacity = models.IntegerField(default=0)
    location = models.CharField(max_length=255)

class user_dashboard_model(models.Model):
    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255)
    weight = models.IntegerField(default=0)
    user_email = models.EmailField(default="sunny@gmail.com")
    user_mobile = models.IntegerField(default="9876351239")
    pickup_latitude = models.FloatField(default=0)
    pickup_longitude = models.FloatField(default=0)
    dropoff_latitude = models.FloatField(default=0)
    dropoff_longitude = models.FloatField(default=0)

class professional_dashboard_model(models.Model):
    accept = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)