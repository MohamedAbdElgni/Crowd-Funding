from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Project
from .forms import ProjectForm

# Create your views here.
users = [
    {
        "id": "1",
        "first_name": "mohamed",
        "fast_name": "ahmed",
        "mail": "mohamed@gmail.com",
        "password": "123465",
        "mobile": "01098557840",
        "profile_pic": "pic1.jpg",
    },
    {
        "id": "2",
        "first_name": "omer",
        "fast_name": "ahmed",
        "mail": "omer@gmail.com",
        "password": "123465",
        "mobile": "01198557840",
        "profile_pic": "pic1.jpg",
    },
    {
        "id": "3",
        "first_name": "ali",
        "fast_name": "ahmed",
        "mail": "ali@gmail.com",
        "password": "123465",
        "mobile": "01298557840",
        "profile_pic": "pic1.jpg",
    },
]

current_user = users[0]

# Create Project ----------------------------------------------->

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'fundprojects/create.html' 
    success_url = reverse_lazy('fundprojects:projects')  

# List All Projects -------------------------------------------->

class ProjectListView(ListView):
    model = Project
    template_name = 'fundprojects/projects.html'
    context_object_name = 'projects'

# Project Details ------------------------------------------------>

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'fundprojects/show.html'
    context_object_name = 'project'
