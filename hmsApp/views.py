from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import CreateUserForm
from django.contrib import messages
from .models import Hotel, Room, Profile, ImageGallery, CheckAvailable
from django.contrib.auth.models import User
from django.db.models import Q
import razorpay
import random
import datetime


# Create your views here.
def index(req):
    hotels = Hotel.objects.all()
    # first_three_hotels = Hotel.objects.all()[:3]
    topRated = Hotel.objects.filter(category__in=["5 Star", "4 Star"])
    first_three_hotels = topRated[:3]
    # Query the next three hotels from the database
    next_three_hotels = topRated[3:6]
    # locations = Hotel.objects.filter()
    context = {
        "hotels": hotels,
        "first_three_hotels": first_three_hotels,
        "topRated": topRated,
        "next_three_hotels": next_three_hotels,
    }

    return render(req, "index.html", context)


def viewHotel(req):
    hotels = Hotel.objects.all()
    context = {}
    context["hotels"] = hotels
    return render(req, "viewHotel.html", context)


def search(req):
    query = req.POST["loc"]
    print(f"Query is {query}")
    if not query:
        result = Hotel.objects.all()
    else:
        result = Hotel.objects.filter(Q(location__icontains=query))
    return render(req, "viewHotel.html", {"results": result, "query": query})


def viewRoom(req, hid):
    hotels = Hotel.objects.get(hotel_id=hid)
    rooms = Room.objects.filter(hotel_id=hid)
    gallery = ImageGallery.objects.filter(hotel_id=hid)
    context = {
        "hotels": hotels,
        "rooms": rooms,
        "gallery": gallery,
    }
    return render(req, "viewRoom.html", context)


def book_room_page(request):
    user = request.user if request.user.is_authenticated else None
    if user:
        room = Room.objects.all().get(room_id=int(request.GET["room_id"]))
        name = Profile.objects.all().get(user=user)
    else:
        return redirect("/login")

    return HttpResponse(render(request, "cart.html", {"room": room, "name": name}))


def book_room(request):
    if request.method == "POST":
        # room_id = Room.objects.get(room_id=rid)
        roomid = request.POST["room_id"]
        room = Room.objects.all().get(room_id=roomid)
        # for finding the reserved rooms on this time period for excluding from the query set
        for each_reservation in CheckAvailable.objects.all().filter(room=room):
            if str(each_reservation.check_in_date) < str(
                request.POST["check_in"]
            ) and str(each_reservation.check_out_date) < str(request.POST["check_out"]):
                pass
            elif str(each_reservation.check_in_date) > str(
                request.POST["check_in"]
            ) and str(each_reservation.check_out_date) > str(request.POST["check_out"]):
                pass
            else:
                messages.warning(request, "Sorry This Room is unavailable for Booking")
                return redirect("check_room_availability", rid=roomid)

        current_user = request.user
        total_person = int(request.POST["person"])
        booking_id = str(roomid) + str(datetime.datetime.now())

        checkAvailable = CheckAvailable()
        room_object = Room.objects.all().get(room_id=roomid)
        room_object.status = "2"

        user_object = User.objects.all().get(username=current_user)

        checkAvailable.user = user_object
        checkAvailable.room = room_object
        person = total_person
        checkAvailable.num_guests = person
        checkAvailable.check_in_date = request.POST["check_in"]
        checkAvailable.check_out_date = request.POST["check_out"]
        checkAvailable.booking_id = booking_id

        checkAvailable.save()

        messages.success(request, "Congratulations! Booking Successfull")

        return redirect("/payment")
    else:
        return HttpResponse("Access Denied")


def makePayment(req):
    checkAvail = CheckAvailable.objects.filter(user=req.user)
    total_price = 0
    for x in checkAvail:
        total_price = x.room.room_price
        booking_id = x.booking_id
    client = razorpay.Client(
        auth=("rzp_test_sUTZ37PTI6oDaZ", "81iQLqkJ2a10ceOpuTfHHSG2")
    )
    data = {"amount": total_price * 100, "currency": "INR", "receipt": booking_id}
    payment = client.order.create(data=data)
    context = {}
    context["data"] = payment
    context["amount"] = payment["amount"]
    # booking.update(is_completed=True)
    return render(req, "payment.html", context)


def check_room_availability(request, rid):
    room = Room.objects.filter(room_id=rid)
    if request.method == "POST":
        try:
            print(request.POST)
            rr = []
            # for finding the reserved rooms on this time period for excluding from the query set
            for each_reservation in CheckAvailable.objects.all():
                if str(each_reservation.check_in_date) < str(
                    request.POST["cin"]
                ) and str(each_reservation.check_out_date) < str(request.POST["cout"]):
                    pass
                elif str(each_reservation.check_in_date) > str(
                    request.POST["cin"]
                ) and str(each_reservation.check_out_date) > str(request.POST["cout"]):
                    pass
                else:
                    rr.append(each_reservation.room.room_id)

            room = (
                Room.objects.all()
                .filter(room_id=rid, max_capacity__gte=int(request.POST["capacity"]))
                .exclude(room_id__in=rr)
            )
            if len(room) == 0:
                messages.warning(
                    request, "Sorry No Rooms Are Available on this time period"
                )
            data = {"rooms": room, "flag": True}
            response = render(request, "checkAvailability.html", data)
        except Exception as e:
            messages.error(request, e)
            response = render(request, "checkAvailability.html", {"room": room})

    else:
        data = {"room": room}
        response = render(request, "checkAvailability.html", data)
    return HttpResponse(response)


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
            phoneNo = request.POST["phoneNo"]
            Profile.objects.create(
                user=user,
                name=name,
                gender=gender,
                profilePic=profilePic,
                dob=dob,
                pincode=pincode,
                state=state,
                address=address,
                phoneNo=phoneNo,
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
        phoneNo = request.POST["phoneNo"]
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
        if phoneNo:
            profile.phoneNo = phoneNo
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


def aclist(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.prod.aclist(hid)
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def nonaclist(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.prod.nonaclist(hid)
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def kingroomlist(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.prod.kingroomlist(hid)
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def queenroomlist(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.prod.queenroomlist(hid)
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def twinroomlist(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.prod.twinroomlist(hid)
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def singleroomlist(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.prod.singleroomlist(hid)
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def doubleroomlist(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.prod.doubleroomlist(hid)
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def doubledoubleroomlist(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.prod.doubledoubleroomlist(hid)
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def priceOrder(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.objects.filter(hotel_id=hid).order_by("room_price")
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def descpriceOrder(req, hid):
    if req.method == "GET":
        hotels = Hotel.objects.get(hotel_id=hid)
        queryset = Room.objects.filter(hotel_id=hid).order_by("-room_price")
        context = {}
        context["rooms"] = queryset
        context["hotels"] = hotels
        return render(req, "viewRoom.html", context)


def register_user(req):
    form = CreateUserForm()
    if req.method == "POST":
        form = CreateUserForm(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, ("User created successfully"))
            return redirect("/login")
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
            messages.error(req, ("Incorrect Username or Password"))
            return redirect("/login")
    else:
        return render(req, "login.html")


def logout_user(req):
    logout(req)
    messages.success(req, ("Logged out Successfully"))
    return redirect("/")


def myBooking(req):
    if req.user.is_authenticated == False:
        return redirect("login")
    user = User.objects.all().get(id=req.user.id)
    print(f"request user id ={req.user.id}")
    bookings = CheckAvailable.objects.all().filter(user=user)
    if not bookings:
        messages.warning(req, "No Bookings Found")
    return render(req, "myBooking.html", {"bookings": bookings})
