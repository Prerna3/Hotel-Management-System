from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe


class CustomeManager(models.Manager):
    def get_location(self, location):
        return self.filter(location__iexact=location)


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


class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.PositiveIntegerField()
    num_rooms = models.PositiveIntegerField()
