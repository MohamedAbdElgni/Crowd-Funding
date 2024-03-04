from django.shortcuts import render

def home(request):
    return render(request, 'fundprojects/main/home.html')