from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

class Hotel(models.Model):
  hotel_id = models.IntegerField(primary_key = True)
  hotel_name = models.CharField(max_length = 50)
  star = (("2 Star","2 Star"),("3 Star","3 Star"),("4 Star","4 Star"),("5 Star","5 Star"))
  category = models.CharField(max_length = 100, choices = star)
  price = models.IntegerField()
  city = (("Mumbai","Mumbai"),("Pune","Pune"),("Bengaluru","Bengaluru"),("Delhi","Delhi"),("Kolkata","Kolkata"),("Jaipur","Jaipur"),("Udaipur","Udaipur"),("Varanasi","Varanasi"),("Chennai","Chennai"),("Ahemdabad","Ahemdabad"),("Patna","Patna"),("Shimla","Shimla"),("Manali","Manali"),("Indore","Indore"),("Lucknow","Lucknow"))
  location = models.CharField(max_length = 100, choices = city)
  desc = models.CharField(max_length = 255)
  image = models.ImageField(upload_to='hotel_pics')

  def proImage(self):
    return mark_safe(f"<img src='{self.image.url}' width='300px'>")
  
  def __str__(self):
    return(f"{self.hotel_name}")