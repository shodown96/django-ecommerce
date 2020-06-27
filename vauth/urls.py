from django.urls import path
from .views import *

app_name = "vauth"
urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("wishlist/", wishlist, name="wishlist"),
    path("orders/", orders, name="orders"),
    path("addresses/", addresses, name="addresses"),
    path("profile/", profile, name="profile"),
]
