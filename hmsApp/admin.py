from django.contrib import admin
from .models import Hotel, ImageGallery, Room, Profile, CheckAvailable


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
        "status",
        "available",
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


class CheckAvailableAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "room_id",
        "check_in_date",
        "check_out_date",
        "num_guests",
        "booking_id",
    )


admin.site.register(CheckAvailable, CheckAvailableAdmin)
