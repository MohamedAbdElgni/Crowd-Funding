from django.shortcuts import render
from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse,HttpResponseRedirect
import re
from .models import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator

@method_decorator(login_required, name='dispatch')
def hello(request):
    return render(request,'welcom.html') 

def register(request):
    if request.user.is_authenticated:
         return redirect('/')

    
    
    all=Register.objects.all()
    Allemail=[]
    for x in all:
         Allemail.append(x.email) 

    if(request.method=="POST"):
        # if(request.POST['lname']!=''):
        fname=request.POST['firstname']
        lname=request.POST['lname']
        # else:
        #     context={'nameError':"Your name must be enterd"}
        #     return render(request,'registerP.html',context)
        if(request.POST['email']!=''):
        
            email=request.POST['email']
        else:
            context={'emailRequierd':'Email is required'}
            return render(request,"registerP.html",context)
        pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$"

        if re.match(pattern, request.POST['email']):
                        
                        email = request.POST['email']

        else:
            context={'emailsentax':"The email should be hello@gmail.com"}


            return render(request, 'RegisterP.html',context)
        
        if(request.POST['email'] in Allemail):
        
            context={'emailExist':"This email aredy exist"}
            return render(request, 'RegisterP.html',context)   

        else:
             email=request.POST['email']

        if(request.POST['password']!=request.POST['confirm_password']):
             context={'passError':"Password and confirm password does not match"}
             return render(request, 'RegisterP.html',context)
        else:
             password=request.POST['password']
             confirm_password=request.POST['confirm_password']   

        if(request.POST['phone']==''):
             
             
            context={'phonerequird':'YOU must enter the phone number'}
            return render(request,'RegisterP.html',context)
        else:
             phone=request.POST['phone'] 

        PHONE_REGEX = r'^01[0-2,5]\d{8}$'

        if re.match(PHONE_REGEX,request.POST['phone']):
             phone=request.POST['phone']            
        else:
             context={'phoneMatch':"This phone do not match Egyption Phone"}





        Register.objects.create(first_name=fname,last_name=lname,email=email,password=password,phone=phone)
        return render(request,'loginP.html')

    return render(request,'RegisterP.html')

def login(request):
     if request.user.is_authenticated:
          return redirect('/')
     Allemails=list(Register.objects.all() )    
     if(request.method=="POST"):
          email=request.POST["email"]
          password=request.POST['password']  
          for x in list(Register.objects.all()):    
            #    print(f"requst email:=={email}")
            #    print(f"db email:=={x.email}")

               if (email==x.email and password==x.password):
                    user=authenticate(request,email=email,password=password)
                    if user:
                         login(request,user)
                         print(user)
                    # context={'username':x.username,}
                    return render(request,'welcom.html')
               else:
                      context={'logineror':"invalid email or password"}
                      return render(request, 'loginP.html',context) 
     return render(request,'loginP.html')

def user_logout(request):
     logout(request)
     return redirect('login')