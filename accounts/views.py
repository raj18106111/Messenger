from django.shortcuts import render , redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
def loginUser(request):
    
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request,user)
            return redirect("/")
        else:
            messages.error(request,"Login Invalid")
            return render(request,'login.html')
    return render(request,'login.html')

def logoutuser(request):
    logout(request)
    return redirect('/accounts/login')

def signupuser(request):
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        email=request.POST.get("email")
        if User.objects.filter(username=username).exists():
            messages.warning(request, 'Username already in use')
            return render(request,'signup.html')
        elif User.objects.filter(email=email).exists():
            messages.warning(request, 'Email already in use')
            return render(request,'signup.html')
        elif username=="":
            messages.warning(request, 'Invalid Username')
            return render(request,'signup.html')
        elif password=="":
            messages.warning(request, 'Invalid Password')
            return render(request,'signup.html')
        else:
            user = User.objects.create_user(username=username,password=password,email=email)
            user.is_active = True
            user.save()
            return redirect('/accounts/login')
    return render(request,'signup.html')

