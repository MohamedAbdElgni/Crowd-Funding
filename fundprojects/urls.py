from django.urls import path
from .views import ProjectCreateView,ProjectListView,ProjectDetailView

app_name = 'fundprojects'
urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', ProjectDetailView.as_view(), name='project_detail'),
]