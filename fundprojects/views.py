from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import *
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

def project_details(request, project_id):
    project = Project.objects.get(id=project_id)
    comments = Comments.get_comments_by_project(project_id)
    return render(request, 'fundprojects/show.html', {'project': project, 'comments': comments})



def add_comment(request, project_id):
    if request.method == 'POST':
        comment = request.POST['comment']
        Comments.objects.create(comment=comment, project_id=project_id, user_id=current_user['id'])
        return redirect('fundprojects:project_details', project_id=project_id)
    else:
        return redirect('fundprojects:project_details', project_id=project_id)
        
def delete_comment(request, project_id, comment_id):
    pass



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


def report_comment(request, comment_id):
    comment = get_object_or_404(Comments, pk=comment_id)
    if request.method == 'POST':
        report = request.POST.get('report')
        if report:
            CommentsReports.objects.create(report=report, comment_id=comment_id, user_id=request.user.id)
            return redirect('fundprojects:project_details', project_id=comment.project.id)
        else:
            return redirect('fundprojects:project_details', project_id=comment.project.id)
    else:
        return render(request, 'fundprojects/report_comment.html', {'comment': comment})
    

def delete_comment(request, project_id, comment_id):
   pass

def donate (request, project_id):
    pass

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

class CategoryProjectsView(ListView):
    model = Project
    template_name = 'fundprojects/category_projects.html'
    context_object_name = 'projects'

    def get_queryset(self):
        category_id = self.kwargs['category_id'] 
        return Project.objects.filter(category_id=category_id)