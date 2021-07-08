from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Profile
from .form import Register_form,Profile_form,Login_form,Edit_form
import requests
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.
local="127.0.0.1:8000"
server="jwtintership.herokuapp.com"
token=""
def register_view(request):
    if request.method == "POST":
        Rform=Register_form(request.POST)
        Pform=Profile_form(request.POST)
        if Rform.is_valid() and Pform.is_valid():
            user = Rform.save()
            profile = Pform.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request,"User created.")
            return redirect("login")
        else:
            messages.error(request,"Invalid Credentials.")
            return redirect("register")
    else:
        Rform=Register_form()
        Pform=Profile_form()
        context={"pform":Pform,"rform":Rform}
        return render(request,'accounts/register.html',context)

def login_view(request):
    if request.method == "POST":
        email = request.POST.get('Email')
        Password = request.POST.get('Password')
        user = User.objects.filter(email=email).first()
        if user is not None:
            data={
            "username": user.username,
            "password" : Password
            }
            link=f"http://{server}/obtaintoken/"
            status=requests.post(link,json=data)
            if status.status_code==200:
                token=status.text.split(",")
                token=token[1][10:len(token[1])-2]
                #print(token)
                response = redirect("home")
                login(request,user)
                response.set_cookie('access',token)
                return response
            else:
                messages.error(request,"Invalid Password.")
                return redirect("login")
        else:
            messages.error(request,"User not found.")
            return redirect("login")
    else:
        form = Login_form()
        return render(request,"accounts/login.html",{'form':form})

def home_view(request):
    if verify(request):
        user=User.objects.all()
        profile=Profile.objects.all()
        detail=[]
        for i in range(len(user)):
            item={
            "user":user[i],
            "profile":profile[i]
            }
            detail.append(item)
        return render(request,"accounts/home.html",{"details":detail})
    else:
        logout(request)
        messages.error(request,"You have been Logout.")
        return redirect('login')

def verify(request):
    link=f"http://{server}/verifytoken/"
    data={
    "token": request.COOKIES['access']
    }
    status=requests.post(link,json=data)
    if status.status_code==200:
        return True
    else:
        return False

def edit_view(request,id):
    if verify(request):
        obj=User.objects.get(id=id)
        obj_pro=Profile.objects.get(user=id)
        print(obj.password)
        if request.method == "POST":
            Rform=Edit_form(request.POST,instance=obj)
            Pform=Profile_form(request.POST,instance=obj_pro)
            if Rform.is_valid() and Pform.is_valid():
                user = Rform.save()
                profile = Pform.save(commit=False)
                profile.user = user
                profile.save()
                messages.success(request,"Details have been updated.")
                return redirect("home")
            else:
                messages.error(request,"Invalid Credentials.")
                return redirect("home")

        else:
            Rform=Edit_form(instance=obj)
            Pform=Profile_form(instance=obj_pro)
            context={"pform":Pform,"rform":Rform}
            return render(request,"accounts/edit.html",context)
    else:
        logout(request)
        messages.error(request,"You have been Logout.")
        return redirect('login')

def delete_view(request,id):
    if verify(request):
        obj=User.objects.get(id=id)
        if request.method == 'POST':
            obj.delete()
            return redirect('home')
        context = {
            'object': obj
        }
        return render(request,'accounts/delete.html',context)
    else:
        logout(request)
        messages.error(request,"You have been Logout.")
        return redirect('login')

def logout_view(request):
    logout(request)
    messages.error(request,"You have been Logout.")
    return redirect('login')
