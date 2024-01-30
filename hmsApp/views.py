from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from django.contrib import messages
from .models import Hotel, Room, Booking, Profile
from django.contrib.auth.models import User


# Create your views here.
def index(req):
    hotels = Hotel.objects.all()
    first_three_hotels = Hotel.objects.all()[:3]

    # Query the next three hotels from the database
    next_three_hotels = Hotel.objects.all()[3:6]
    # locations = Hotel.objects.filter()
    context = {
        "hotels": hotels,
        "first_three_hotels": first_three_hotels,
        "next_three_hotels": next_three_hotels,
    }

    return render(req, "index.html", context)


def viewHotel(req):
    hotels = Hotel.objects.all()
    context = {}
    context["hotels"] = hotels
    return render(req, "viewHotel.html", context)


def search(req):
    if req.method == "GET":
        return redirect("/")
    else:
        loc = req.POST.get("loc")
        if loc:
            queryset = Hotel.prod.get_location(loc)
            print(queryset)
            context = {
                "hotels": queryset,
                "loc": loc,
            }
            return render(req, "viewHotel.html", context)
        else:
            return redirect("/")


def viewRoom(req):
    # hotels = Hotel.objects.get(hotel_id=rid)
    rooms = Room.objects.all()
    context = {
        # "hotels": hotels,
        "rooms": rooms,
    }
    return render(req, "viewRoom.html", context)


def profile(req, user_id):
    profile_object = get_object_or_404(User, pk=user_id)
    profile = Profile.objects.get(user=profile_object)
    user = profile.user

    current_user = req.user
    is_current_user = current_user == user
    context = {
        "user": user,
        "profile_object": profile_object,
        "profile": profile,
        "is_current_user": is_current_user,
    }
    return render(req, "profile.html", context)


def createProfile(request):
    user = request.user
    profile_exists = Profile.objects.filter(user=user).exists()
    if not profile_exists:
        if request.method == "POST":
            user = request.user
            name = request.POST["name"]
            gender = request.POST["gender"]
            profilePic = request.FILES["profilePic"]
            dob = request.POST["dob"]
            pincode = request.POST["pincode"]
            state = request.POST["state"]
            address = request.POST["address"]
            Profile.objects.create(
                user=user,
                name=name,
                gender=gender,
                profilePic=profilePic,
                dob=dob,
                pincode=pincode,
                state=state,
                address=address,
            )
            return redirect("profile", user_id=user.id)
        else:
            return render(request, "profile.html")
    else:
        return redirect("profile", user_id=user.id)


def editProfile(request, user):
    user = request.user
    profile = get_object_or_404(Profile, user=user)
    if request.method == "POST":
        name = request.POST["name"]
        gender = request.POST["gender"]
        profilePic = request.FILES["profilePic"]
        dob = request.POST["dob"]
        pincode = request.POST["pincode"]
        state = request.POST["state"]
        address = request.POST["address"]
        if name:
            profile.name = name
        if gender:
            profile.gender = gender
        if profilePic:
            profile.profilePic = profilePic
        if dob:
            profile.dob = dob
        if pincode:
            profile.pincode = pincode
        if state:
            profile.state = state
        if address:
            profile.address = address
        profile.save()
        return redirect("profile", user_id=user.id)

    return render(request, "profile.html", {"profile": profile})


def range(req):
    if req.method == "GET":
        return redirect("/viewRoom")
    else:
        min = req.POST["min"]
        max = req.POST["max"]
        if min != "" and max != "" and min is not None and max is not None:
            queryset = Room.prod.get_price_range(min, max)
            context = {}
            context["rooms"] = queryset
            return render(req, "viewRoom.html", context)
        else:
            return redirect("/viewRoom")


def aclist(req):
    if req.method == "GET":
        queryset = Room.prod.aclist()
        context = {}
        context["rooms"] = queryset
        return render(req, "viewRoom.html", context)


def nonaclist(req):
    if req.method == "GET":
        queryset = Room.prod.nonaclist()
        context = {}
        context["rooms"] = queryset
        return render(req, "viewRoom.html", context)


def kingroomlist(req):
    if req.method == "GET":
        queryset = Room.prod.kingroomlist()
        context = {}
        context["rooms"] = queryset
        return render(req, "viewRoom.html", context)


def queenroomlist(req):
    if req.method == "GET":
        queryset = Room.prod.queenroomlist()
        context = {}
        context["rooms"] = queryset
        return render(req, "viewRoom.html", context)


def twinroomlist(req):
    if req.method == "GET":
        queryset = Room.prod.twinroomlist()
        context = {}
        context["rooms"] = queryset
        return render(req, "viewRoom.html", context)


def singleroomlist(req):
    if req.method == "GET":
        queryset = Room.prod.singleroomlist()
        context = {}
        context["rooms"] = queryset
        return render(req, "viewRoom.html", context)


def doubleroomlist(req):
    if req.method == "GET":
        queryset = Room.prod.doubleroomlist()
        context = {}
        context["rooms"] = queryset
        return render(req, "viewRoom.html", context)


def doubledoubleroomlist(req):
    if req.method == "GET":
        queryset = Room.prod.doubledoubleroomlist()
        context = {}
        context["rooms"] = queryset
        return render(req, "viewRoom.html", context)


def priceOrder(req):
    queryset = Room.objects.all().order_by("room_price")
    context = {}
    context["rooms"] = queryset
    return render(req, "viewRoom.html", context)


def descpriceOrder(req):
    queryset = Room.objects.all().order_by("-room_price")
    context = {}
    context["rooms"] = queryset
    return render(req, "viewRoom.html", context)


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


def myBooking(req):
    return render(req, "myBooking.html")
