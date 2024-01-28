from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("viewHotel/", views.viewHotel, name="viewHotel"),
    path("myProfile/", views.myProfile, name="myProfile"),
    path("viewRoom/", views.viewRoom, name="viewRoom"),
    path("search/", views.search, name="search"),
]
