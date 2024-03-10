from django.shortcuts import render
from fundprojects.models import *

def home(request):
    # 5 featured projects by admin
    # 5 latest projects
    lts_projects = Project.objects.all().order_by('-id')[:5]
    categories = Category.objects.all()
    feat= Project.objects.filter(featured=True)
    top_rated = Project.get_top_rated_projects()
    
    return render(request, 'fundprojects/home.html', {'categories':categories, 'lts_projects':lts_projects, 'feat':feat, 'top_rated':top_rated})