from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_user, name="register"),
    path("login", views.login_user, name="login"),
    path("logout", views.logout_user, name="logout"),
    path("viewHotel/", views.viewHotel, name="viewHotel"),
    path("viewRoom/", views.viewRoom, name="viewRoom"),
    path("search/", views.search, name="search"),
    path("priceOrder", views.priceOrder, name="priceOrder"),
    path("descpriceOrder", views.descpriceOrder, name="descpriceOrder"),
    path("aclist", views.aclist, name="aclist"),
    path("nonaclist", views.nonaclist, name="nonaclist"),
    path("kingroomlist", views.kingroomlist, name="kingroomlist"),
    path("queenroomlist", views.queenroomlist, name="queenroomlist"),
    path("twinroomlist", views.twinroomlist, name="twinroomlist"),
    path("singleroomlist", views.singleroomlist, name="singleroomlist"),
    path("doubleroomlist", views.doubleroomlist, name="doubleroomlist"),
    path(
        "doubledoubleroomlist", views.doubledoubleroomlist, name="doubledoubleroomlist"
    ),
    path("range", views.range, name="range"),
    path("profile/<int:user_id>/", views.profile, name="profile"),
    path("createprofile/", views.createProfile, name="createprofile"),
    path("editprofile/<user>/", views.editProfile, name="editprofile"),
    path("myBooking", views.myBooking, name="myBooking"),
]
