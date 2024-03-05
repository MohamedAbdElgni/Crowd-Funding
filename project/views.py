from django.shortcuts import render
from fundprojects.models import *

def home(request):
    categories = Category.objects.all()
    return render(request, 'fundprojects/home.html', {'categories':categories})