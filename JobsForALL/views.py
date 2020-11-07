from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse


from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


#  importing models

from .models import User,UserProfile

import json

# Some Quotes

Login_quote = 'Think about a quote for here sayan'
register_quote = 'Think about a quote for here sayan'

# some util functions
def content_valid_check(content):
    if len(content) == 0:
        return False
    
    check = 0    
    for i in content:
        if i != ' ':
            check = 1
    if check == 0:
        return False
    else:
        return True

def handle_json_request(request,data):
    if data['type'] == 'edit-profile':
        try:
            user_requested =  User.objects.get(pk= int(data['pk']))
            if user_requested != request.user :
                return 
            user_requested_profile = UserProfile.objects.get(user=user_requested)
            user_requested_profile.name = data['name']
            user_requested_profile.location = data['location']
            user_requested_profile.service_type = data['service']
            user_requested_profile.save()

        except User.DoesNotExist:
            return 



# Create your views here.

def index(request):
    return HttpResponse("Hello, world!")


# login view 
def login_view(request):

    if request.method == 'POST':

        # Attempt to sign in user 

        username = request.POST["username"] 
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)   

        # Check if authentication was a success
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request,"JobsForALL/login.html",{ "message":"Invalid username and/or password.",'quote':Login_quote})  
    else:
        return render(request,'JobsForALL/login.html',{'quote':Login_quote})          

# log-out view
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index")) 

# sign-up view
def register(request):

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname =request.POST["fullname"]
        usertype =  request.POST['Usertype']


        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if password != confirmation:
            return render(request,"JobsForALL/register.html",{
            "message": "Passwords Must match."
            })
        
        #  Attempt to create new user
        try:
            user = User.objects.create_user(username,email,password)
            user.save()
        except IntegrityError:
            return render(request,"JobsForALL/register.html",{
            "message": "Sorry,username already taken.",'quote':register_quote
            })       
        userProfile = UserProfile(user=user)
        userProfile.name = firstname
        userProfile.usertype = usertype
        userProfile.save()

        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"JobsForALL/register.html",{'quote':register_quote})       


def user_view(request,pk):
   
    if request.method == 'PUT':
        data = json.loads(request.body)
        handle_json_request(request,data)

    """
    if request.method == 'POST' and request.FILES['file']:
        x = User_profile.objects.get(user=request.user)
        x.profile_image = request.FILES['file']
        x.save()
    """
    try:
        requested_user = User.objects.get(pk=pk)

        # check if the user if trying to view thier own profile
        self_view = False
        if requested_user == request.user:
            self_view = True
                       
        message = ''    
        try: 
            if requested_user.userprofile.location == 'Not Set Yet':
                message = 'Your profile is still incomplete..'
        except:
            pass
        employee = False    
        if requested_user.userprofile.usertype == 'employee':
            employee = True

       

        return render(request,"JobsForALL/profile.html",{
            "requested_user":requested_user,
            'self_view':self_view,'message':message,'employee':employee

        }) 
    
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index")) 