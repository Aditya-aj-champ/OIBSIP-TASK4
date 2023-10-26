# from os import login_tty
# from telnetlib import LOGOUT
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def home(request):
    return render(request,"index.html")

def signup(request):

    if request.method == "POST":
        username = request.POST['username']
        email= request.POST['email']
        fname= request.POST['fname']
        lname= request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request,"Username alredy exist!try another ")
            return redirect('signup') 
        
        if username.isalnum():
            messages.error(request,"username must be Alpha-Numerice!")
            return redirect('signup')
        
        if len(username)>20:
            messages.error(request,"username must be under 20 characters")
            return redirect('signup')

        
        if User.objects.filter(email=email):
            messages.error(request,"Email already registered!")
            return redirect('signup')
        


        if pass1!=pass2:
            messages.error(request,"password didn't match")
            return redirect('signup')

        

        myuser = User.objects.create_user(username,email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()
        messages.success(request, "your Account has been successfully created")
        return redirect('signin')
    
    return render(request,"signup.html") 

def signin(request):
    if request.method == "POST":
        username= request.POST['username']
        pass1 = request.POST['pass1']


        # if User.objects.filter(username=username):
        #     messages.error(request,"Username alredy exist! plese try some other username")
        #     return redirect('index')

        user = authenticate(username = username, password = pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name

            return render(request, "index.html",{'fname':fname})

        else:
            messages.error(request, "Invalid UserName & Password")  
            return redirect('signin')
            

    return render(request,"signin.html")

def signout(request):
    logout(request)
    messages.success(request, "loggout successfully!")
    return redirect('index')