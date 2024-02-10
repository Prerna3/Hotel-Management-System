from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe


class CustomeManager(models.Manager):
    def get_price_range(self, r1, r2):
        return self.filter(room_price__range=(r1, r2))

    def get_location(self, location):
        return self.filter(location__iexact=location)

    def aclist(self, hid):
        return self.filter(ac_room__exact="AC", hotel_id__exact=hid)

    def nonaclist(self, hid):
        return self.filter(ac_room__exact="Non-AC", hotel_id__exact=hid)

    def kingroomlist(self, hid):
        return self.filter(room_category__exact="King Room", hotel_id__exact=hid)

    def queenroomlist(self, hid):
        return self.filter(room_category__exact="Queen Room", hotel_id__exact=hid)

    def twinroomlist(self, hid):
        return self.filter(room_category__exact="Twin Room", hotel_id__exact=hid)

    def singleroomlist(self, hid):
        return self.filter(room_category__exact="Single Room", hotel_id__exact=hid)

    def doubleroomlist(self, hid):
        return self.filter(room_category__exact="Double Room", hotel_id__exact=hid)

    def doubledoubleroomlist(self, hid):
        return self.filter(
            room_category__exact="Double-Double Room", hotel_id__exact=hid
        )


class Hotel(models.Model):
    hotel_id = models.IntegerField(primary_key=True)
    hotel_name = models.CharField(max_length=50)
    star = (
        ("2 Star", "2 Star"),
        ("3 Star", "3 Star"),
        ("4 Star", "4 Star"),
        ("5 Star", "5 Star"),
    )
    category = models.CharField(max_length=100, choices=star)
    price = models.IntegerField()
    location = models.CharField(max_length=100)
    desc = models.CharField(max_length=255)
    image = models.ImageField(upload_to="hotel_pics")

    prod = CustomeManager()  # customer manager
    objects = models.Manager()  # default manager

    def proImage(self):
        return mark_safe(f"<img src='{self.image.url}' width='300px'>")

    def __str__(self):
        return f"{self.hotel_name}"


class ImageGallery(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    imagegallery = models.ImageField(upload_to="hotelroom_gallery")

    def galleryImage(self):
        return mark_safe(f"<img src='{self.imagegallery.url}' width='300px'>")

    def __str__(self):
        return f"Image for {self.hotel.hotel_name}"


class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_id = models.IntegerField(primary_key=True)
    room_name = models.CharField(max_length=50)
    room_status = (
        ("1", "available"),
        ("2", "not available"),
    )
    type = {
        ("King Room", "King Room"),
        ("Queen Room", "Queen Room"),
        ("Single Room", "Single Room"),
        ("Double Room", "Double Room"),
        ("Double-Double Room", "Double-Double Room"),
        ("Twin Room", "Twin Room"),
    }
    room_category = models.CharField(max_length=20, choices=type)
    room_contain = {("AC", "AC"), ("Non-AC", "Non-AC")}
    ac_room = models.CharField(max_length=10, choices=room_contain, default=True)
    max_capacity = models.IntegerField(default=1)
    room_price = models.IntegerField()
    roomImage = models.ImageField(upload_to="room_pics")
    status = models.CharField(choices=room_status, max_length=15, default=True)
    available = models.BooleanField(default=True)

    prod = CustomeManager()
    objects = models.Manager()

    def roomImages(self):
        return mark_safe(f"<img src='{self.roomImage.url}' width='300px'>")

    def _str_(self):
        return f"{self.room_id}.{self.room_category} with {self.beds} beds for {self.max_capacity} people"


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=30, blank=True, null=True)
    gender = models.CharField(max_length=30, blank=True, null=True)
    address = models.TextField(max_length=200, blank=True)
    profilePic = models.ImageField(upload_to="profilePic", default=None)
    pincode = models.CharField(max_length=30, blank=True, null=True)
    state = models.CharField(max_length=30, blank=True, null=True)
    dob = models.DateField()
    phoneNo = models.CharField(max_length=10, blank=True, null=True)

    def _str_(self):
        return f"{self.user} has name {self.name} gender {self.gender} dob {self.dob} state {self.state} pincode {self.pincode}"


class CheckAvailable(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, default=True)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    booking_id = models.CharField(max_length=100, default="null")

    def __str__(self):
        return self.user.username
