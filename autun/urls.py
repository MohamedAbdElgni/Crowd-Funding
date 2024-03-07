from django.urls import path
from .views import *
urlpatterns = [
   
    path('',hello),
    path('register',register),
    path('login',login)
]