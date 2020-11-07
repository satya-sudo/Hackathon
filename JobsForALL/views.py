from django.shortcuts import render,HttpResponseRedirect
from django.http import HttpResponse
from django.urls import reverse


from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError


#  importing models

from .models import User,Employer,Employee

# Some Quotes

Login_quote = 'Think about a quote for here sayan'
register_quote = 'Think about a quote for here sayan'

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

        if usertype == 'employer':
            values = Employer(user=user)
            values.name = firstname
            values.save()
            
        elif usertype == 'employee':
            values = Employee(user=user)
            values.name = firstname
            values.save()
        login(request,user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request,"JobsForALL/register.html",{'quote':register_quote})       


