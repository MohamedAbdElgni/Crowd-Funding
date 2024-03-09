from django.shortcuts import get_object_or_404, render , redirect
from django.contrib import messages

from authentication.token import AccountActivationTokenGenerator
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
        print(user)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, f'Account activated successfully. Please login to continue')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        
        
    return redirect('/')
# Create your views here.
def activation_email(request, user, email):
    mail_subject = 'Activate your account.'
    mail_msg = render_to_string('registration/activation_email.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http',
    })
    email = EmailMessage(
        mail_subject, mail_msg, to=[email]
    )
    if email.send(fail_silently=False):
        messages.success(request, f'Account created successfully. Please check {user.email} to activate your account')
    else:
        messages.error(request, f'Failed to send activation email to {email}')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activation_email(request, user,form.cleaned_data['email'])
            return redirect('/')
    
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect('/')
                else:
                    messages.error(request, 'Please activate your account first')
            else:
                messages.error(request, 'Invalid username or password')
                
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout(request):
    auth_logout(request)
    return redirect('/')