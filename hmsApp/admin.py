from django.contrib import admin
from .models import Hotel, Booking


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


class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "hotel_id",
        "check_in_date",
        "check_out_date",
        "num_guests",
        "num_rooms",
    )


admin.site.register(Booking, BookingAdmin)
