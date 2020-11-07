from django.contrib.auth.models import AbstractUser

from django.db import models

usertypes = (
    ('employer','employer'),
    ('employee','employee')
)

service_type = (
    ('NULL','NULL'),
    ('woodworker','woodworker'),
    ('plumber','plumber'),
    ('electricion','electricion')
    
)

class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(blank=True,default="Not Set Yet",max_length=25)
    location =  models.CharField(blank=True,default="Not Set Yet",max_length=30)
    usertype = models.CharField(max_length=35,choices=usertypes,default='employer')
    service_type = models.CharField(max_length=40,choices=service_type,default='NULL')



class Gig(models.Model):
    Poster = models.ForeignKey(User,on_delete=models.CASCADE,related_name='gigs')
    title =  models.CharField(max_length=40,default='Untitled')
    description = models.TextField(blank = True)
    gig_type =  models.CharField(max_length=40,choices=service_type,default='NULL')
    location =  models.CharField(blank=True,default="Not Set Yet",max_length=30)
    active = models.BooleanField(default=True)
    assign =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='gigs_asigned')


