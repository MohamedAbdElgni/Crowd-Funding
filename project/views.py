from django.shortcuts import render
from fundprojects.models import *

def home(request):
    # 5 featured projects by admin
    # 5 latest projects
    categories = Category.objects.all()
    return render(request, 'fundprojects/home.html', {'categories':categories})