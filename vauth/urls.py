from django.urls import path
from .views import *

app_name = "vauth"
urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("wishlist/", wishlist, name="wishlist"),
    path("orders/", orders, name="orders"),
    path("addresses/", addresses, name="addresses"),
    path("profile/", profile, name="profile"),
    path("address/delete/<int:ad_id>/", delete_address, name="del_addr"),
    path("address/edit/<int:ad_id>/", edit_address, name="edit_addr"),
]
