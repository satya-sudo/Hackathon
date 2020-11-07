from django.contrib.auth.models import AbstractUser

from django.db import models

# User model auth.

class User(AbstractUser):
    pass


class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(blank=True,default="Not Set Yet",max_length=25)
    location =  models.CharField(blank=True,default="Not Set Yet",max_length=30)

class Employee(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(blank=True,default="Not Set Yet",max_length=25)
    location =  models.CharField(blank=True,default="Not Set Yet",max_length=30)
    