from django.urls import path
from .views import *

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path("profile/", profile, name="profile"),
    path("delete_profile/", delete_profile, name="delete_profile"),
    path("delete_project/<int:id>/", delete_project, name="delete_project"),
    path("search/", search, name="search"),
]