from django.urls import path
from .views import *

app_name = 'fundprojects'
urlpatterns = [
    path('', ProjectListView.as_view(), name='projects'),
    path('create/', ProjectCreateView.as_view(), name='project_create'),
    path('<int:project_id>/', project_details , name='project_details'),
    path('comment/<int:project_id>/', add_comment , name='add_comment'),
    path('report/<int:project_id>/', report_project , name='report_project'),
    path('reportcomment/<int:comment_id>/', report_comment , name='report_comment'),
    path('<int:pk>/update/', ProjectUpdateView.as_view(), name='project_update'),
    path('categories/', CategoryListView.as_view(), name='categories'),
    path('donate/<int:project_id>/', donate , name='donate'),
    path('rate/<int:project_id>/', rate_project , name='rate_project'),
]
