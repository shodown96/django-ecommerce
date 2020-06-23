from django.urls import path, include
from .views import *

app_name = "payment"
urlpatterns = [
    path("pay/", pay, name="pay"),
    path("callback/verify/", callback, name="verify"),
    path('cancel/', cancel, name="cancel")
]
