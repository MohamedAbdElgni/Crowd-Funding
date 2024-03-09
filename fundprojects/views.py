from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        files = request.FILES.getlist("image")
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            form.save_m2m()
            for i in files:
                ProjectPicture.objects.create(project=f, image=i)
            messages.success(request, "New Project Added",extra_tags='success')
            return redirect('fundprojects:projects')
        else:
            print(form.errors)
    else:
        form = ProjectForm()
        imageform = ImageForm()

    return render(request, 'fundprojects/create.html', {'form': form , 'imageform':imageform})
    

# List All Projects -------------------------------------------->

class ProjectListView(ListView):
    model = Project
    template_name = 'fundprojects/projects.html'
    context_object_name = 'projects'

# Update Project ------------------------------------------------------------->

class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    
    template_name = 'fundprojects/update.html'
    success_url = reverse_lazy('fundprojects:projects')

# List All Categories --------------------------------------------------------->

class CategoryListView(ListView):
    model = Category
    template_name = 'fundprojects/categories.html'
    context_object_name = 'categories'

# Categorys' Products ----------------------------------------------------------->
    
def category_projects_view(request, category_id):
    projects = Project.objects.filter(category_id=category_id)
    category = get_object_or_404(Category, id=category_id)
    context = {
        'projects': projects,
        'category': category,
    }
    return render(request, 'fundprojects/category_projects.html', context)

# Project Details ------------------------------------------------>
    
def project_details(request, project_id):
    # add 5 related projects based on tage
    # project = Project.objects.get(id=project_id)
    project = get_object_or_404(Project, pk=project_id)
    comments = Comments.get_comments_by_project(project_id)
    total_donations = Donations.get_sum_of_donations(project_id)
    avg_rating = Rating.get_avg_rating(project_id)
    return render(request, 'fundprojects/show.html', {'project': project,
                                                    'comments': comments, 
                                                    'total_donations': total_donations, 
                                                    'avg_rating': avg_rating})

@login_required
def add_comment(request, project_id):
    if request.method == 'POST':
        comment = request.POST['comment']
        Comments.objects.create(comment=comment, project_id=project_id, user_id=current_user['id'])
        messages.success(request, 'Thank you for your comment',extra_tags='success')
        return redirect('fundprojects:project_details', project_id=project_id)
    else:
        return redirect('fundprojects:project_details', project_id=project_id)
        
def delete_comment(request, project_id, comment_id):
    pass


@login_required
def report_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)  
    if request.method == 'POST':
        report = request.POST.get('report')
        if report:
            ProjectsReports.objects.create(report=report, project_id=project_id, user_id=request.user.id)
            return redirect('fundprojects:project_details', project_id=project_id)
        else:
            return redirect('fundprojects:project_details', project_id=project_id)  
    else:
        return render(request, 'fundprojects/report_project.html', {'project': project})

@login_required
def report_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.method == 'POST':
        report = request.POST.get('report')
        if report:
            CommentsReports.objects.create(report=report, comment_id=comment_id, user_id=current_user['id'])
            return redirect('fundprojects:project_details', project_id=comment.project.id)
        else:
            return redirect('fundprojects:project_details', project_id=comment.project.id)
    else:
        return render(request, 'fundprojects/report_comment.html', {'comment': comment})
    

def delete_comment(request, project_id, comment_id):
   pass

@login_required
def donate(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        amount = request.POST.get('amount')
        if amount:
            Donations.objects.create(amount=float(amount), project_id=project_id, user_id=current_user['id'])
            messages.success(request, 'Thank you for your donation')
            return redirect('fundprojects:project_details', project_id=project_id)
        else:
            messages.error(request, 'Please enter valid amount')
            return redirect('fundprojects:project_details', project_id=project_id)
        
@login_required
def rate_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        if int(rating)>=1 and int(rating)<=5:
            if Rating.objects.filter(project_id=project_id, user_id=current_user['id']).exists():
                Rating.objects.filter(project_id=project_id, user_id=current_user['id']).update(rating=rating)
                messages.success(request, 'Rating updated successfully')
            else:
                Rating.objects.create(rating=rating, project_id=project_id, user_id=current_user['id'])
                messages.success(request, 'Thank you for your rating')
            
            return redirect('fundprojects:project_details', project_id=project_id)
        else:
            messages.error(request, 'Please enter valid rating', extra_tags='danger')
            return redirect('fundprojects:project_details', project_id=project_id)
    else:
        return redirect('fundprojects:project_details', project_id=project_id)
    