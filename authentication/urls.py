from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
]