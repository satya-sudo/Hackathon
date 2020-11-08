from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse


from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


#  importing models

from .models import User,UserProfile,Gig

import json

# Some Quotes

Login_quote = '“Technology now allows people to connect anytime, anywhere, to anyone in the world, from almost any device. This is dramatically changing the way people work, facilitating 24/7 collaboration with colleagues who are dispersed across time zones, countries, and continents.”'
register_quote = '“Technology now allows people to connect anytime, anywhere, to anyone in the world, from almost any device. This is dramatically changing the way people work, facilitating 24/7 collaboration with colleagues who are dispersed across time zones, countries, and continents.”'

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
    elif data['type'] == 'closeGig':
        print(data['pk'])
        try:
            gig = Gig.objects.get(pk=int(data['pk']))
            gig.active = False
            gig.save()
            print(data['pk'])
        except:
            pass


    elif data['type'] == 'declineGig':
        try:
            gig = Gig.objects.get(pk=int(data['pk']))
            gig.assign =  None
            gig.save()       
        except:
            pass

# Create your views here.

def index(request):
    return render(request,'JobsForALL/index.html')

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
        phonenummber = request.POST['phonenumber']

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
        userProfile.phone_number =phonenummber
        userProfile.save()

        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"JobsForALL/register.html",{'quote':register_quote})       


def user_view(request,pk):
    
    message = ''  

    if request.method == 'PUT':
        data = json.loads(request.body)
        handle_json_request(request,data)

    
    if request.method == 'POST':
        
        try:
            logged_user  = User.objects.get(pk=request.user.pk)
        except:
            return HttpResponseRedirect(reverse("index"))
        if logged_user.pk == pk:
            title = request.POST['Title']
            discription  = request.POST['discription']
            gigtype = request.POST['gigtype']
            location =  request.POST['location']
            if (content_valid_check(title) and content_valid_check(discription) and content_valid_check(gigtype) and  content_valid_check(location)) == False:
                message += 'Gig not posted , fields missing!! <br> '
            else:
                gig  = Gig(poster=logged_user)
                gig.title = title
                gig.location = location
                gig.description = discription
                gig.gig_type = gigtype
                gig.save()
                message += 'Gig Posted <br>'
            
    try:
        requested_user = User.objects.get(pk=pk)

        # check if the user if trying to view thier own profile
        self_view = False
        if requested_user == request.user:
            self_view = True
                       
          
        try: 
            if requested_user.userprofile.location == 'Not Set Yet' and self_view:
                message = 'Your profile is still incomplete..'
        except:
            pass
        employee = False    
        if requested_user.userprofile.usertype == 'employee':
            employee = True
            all_gigs =  Gig.objects.all().filter(assign=requested_user,active=False).order_by('-created_on')
            try:
                AssignGig = Gig.objects.all().filter(assign=requested_user,active=True).order_by('-created_on')[0]
            except:
                AssignGig = False
            print(employee)
            #print(AssignGig.location)
        else:
            all_gigs =  Gig.objects.all().filter(poster=requested_user).order_by('-created_on')
            AssignGig = False



        return render(request,"JobsForALL/profile.html",{
            "requested_user":requested_user,
            'self_view':self_view,'message':message,'employee':employee,'all_gigs':all_gigs,'AssignGig':AssignGig}) 

    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("index")) 