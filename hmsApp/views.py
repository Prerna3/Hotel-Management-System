from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from django.contrib import messages


# Create your views here.
def index(req):
    return render(req, "index.html")

def viewHotel(req):
    return render(req,"viewHotel.html")

def viewRoom(req):
    return render(req,"viewRoom.html")

def myProfile(req):
    return render(req,"profile.html")

def register_user(req):
    form = CreateUserForm()
    if req.method == "POST":
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, ("User created successfully"))
            return redirect("/")
        else:
            messages.error(req, ("Incorrect Username or Password Format"))
    context = {"form": form}
    return render(req, "register.html", context)


def login_user(req):
    if req.method == "POST":
        username = req.POST["username"]
        password = req.POST["password"]
        user = authenticate(req, username=username, password=password)
        if user is not None:
            login(req, user)
            messages.success(req, ("Logged in Successfully"))
            return redirect("/")
        else:
            messages.error(req, ("There is error"))
            return redirect("/login")
    else:
        return render(req, "login.html")


def logout_user(req):
    logout(req)
    messages.success(req, ("Logged out Successfully"))
    return redirect("/")
