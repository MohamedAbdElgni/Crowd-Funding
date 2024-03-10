from django.shortcuts import get_object_or_404, render , redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Q

from fundprojects.models import Donations, Project
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from .token import account_activation_token
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from .models import *
from django.contrib.auth.decorators import login_required



def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
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

def activation_email(request, user, email):
    mail_subject = 'Activate your account.'
    mail_msg = render_to_string('registration/template_activate_account.html', {
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
        profile = Profile()
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            profile.user = user
            profile.phone = form.cleaned_data['mobile_phone']
            profile.save()
            activation_email(request, user,form.cleaned_data['email'])
            return redirect('/')
    
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})



def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return redirect(reverse('home'))  # Redirect to the home page
                else:
                    messages.error(request, 'Please activate your account first')
            else:
                messages.error(request, 'Invalid username or password')
                
        else:
            messages.error(request, 'Invalid form submission')
    else:
        form = LoginForm()
    
    return render(request, 'registration/login.html', {'form': form})

@login_required
def logout(request):
    auth_logout(request)
    return redirect('/')

@login_required
def profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect(reverse('profile'))
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'registration/profile.html', {'form': form, 'profile': profile})


@login_required
def delete_profile(request):
    current_user = request.user
    profile = Profile.objects.get(user=current_user)
    user = User.objects.get(username=current_user)
    if request.method == 'POST':
        password = request.POST['password']
        if user.check_password(password):
            user.delete()
            messages.success(request, 'Account deleted successfully')
            return redirect('/')
        else:
            messages.error(request, 'Invalid password', extra_tags='danger')
    return render(request, 'registration/delete_account_form.html', {'profile': profile})

@login_required(login_url='login')
def delete_project(request, id):
    project = Project.objects.get(pk=id)
    p_target = project.total_target if project.total_target else 0
    all_donations = Donations.get_sum_of_donations(id) if Donations.get_sum_of_donations(id) else 0
    if request.user == project.user:
        if float(all_donations) < (float(p_target) * 0.25):
            project.delete()
            messages.success(request, 'Project deleted successfully')
            return redirect(reverse('home'))
        else:
            messages.error(request, 'You can not delete this project because it has received donations', extra_tags='danger')
            return redirect(reverse('home'))
    else:
        messages.error(request, 'You are not authorized to delete this project', extra_tags='danger')
        return redirect(reverse('home'))
    



@login_required(login_url='login')
def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        if query:
            projects = Project.objects.filter(Q(title__icontains=query) | Q(category__name__icontains=query))
            return render(request, 'fundprojects/search.html', {'projects': projects, 'query': query})
        else:
            return render(request, 'fundprojects/search.html', {'projects': [], 'query': None})
