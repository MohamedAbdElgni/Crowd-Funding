from django.shortcuts import render
from fundprojects.models import *

def home(request):
    # 5 featured projects by admin
    # 5 latest projects
    lts_projects = Project.objects.all()[:5]
    categories = Category.objects.all()
    print(lts_projects)
    
    return render(request, 'fundprojects/home.html', {'categories':categories, 'lts_projects':lts_projects})