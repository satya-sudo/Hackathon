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
    ('electricion','electricion'),
    ('Rajmistri','Rajmistri')
    
)

class User(AbstractUser):
    pass


class UserProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True)
    name = models.CharField(blank=True,default="Not Set Yet",max_length=25)
    location =  models.CharField(blank=True,default="Not Set Yet",max_length=30)
    usertype = models.CharField(max_length=35,choices=usertypes,default='employer')
    service_type = models.CharField(max_length=40,choices=service_type,default='NULL')
    phone_number = models.CharField(max_length=10,null=True,blank=True)


class Gig(models.Model):
    poster = models.ForeignKey(User,on_delete=models.CASCADE,related_name='gigs')
    title =  models.CharField(max_length=40,default='Untitled')
    description = models.TextField(blank = True)
    gig_type =  models.CharField(max_length=40,choices=service_type,default='NULL')
    location =  models.CharField(blank=True,default="Not Set Yet",max_length=30)
    active = models.BooleanField(default=True)
    assign =  models.ForeignKey(User,on_delete=models.CASCADE,related_name='gigs_asigned',blank=True,null=True)
    created_on =  models.DateTimeField(auto_now_add=True)
