from django.contrib import admin
from . models import Hotel
# Register your models here.
class HotelAdmin(admin.ModelAdmin):
  list_display = ["hotel_id","hotel_name","category","price","location","proImage"]
  
admin.site.register(Hotel,HotelAdmin)
