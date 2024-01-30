from django.contrib import admin
from .models import Hotel, ImageGallery, Room, Booking, Profile


# Register your models here.
class HotelAdmin(admin.ModelAdmin):
    list_display = [
        "hotel_id",
        "hotel_name",
        "category",
        "price",
        "location",
        "proImage",
    ]
    list_filter = ("location",)


admin.site.register(Hotel, HotelAdmin)


class ImageGalleryAdmin(admin.ModelAdmin):
    list_display = ["hotel_id", "galleryImage"]


admin.site.register(ImageGallery, ImageGalleryAdmin)


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "room_id",
        "check_in_date",
        "check_out_date",
        "num_guests",
        "num_rooms",
    )


admin.site.register(Booking, BookingAdmin)


class RoomAdmin(admin.ModelAdmin):
    list_display = (
        "hotel_id",
        "room_id",
        "room_name",
        "room_category",
        "ac_room",
        "max_capacity",
        "room_price",
        "roomImages",
    )


admin.site.register(Room, RoomAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "name",
        "gender",
        "dob",
        "address",
        "state",
        "pincode",
        "phoneNo",
    )


admin.site.register(Profile, ProfileAdmin)
