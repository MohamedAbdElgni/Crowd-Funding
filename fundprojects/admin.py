from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Category)
admin.site.register(Project)
admin.site.register(ProjectPicture)
admin.site.register(Comments)
admin.site.register(ProjectsReports)
admin.site.register(CommentsReports)
admin.site.register(Donations)
admin.site.register(Rating)
#admin.site.register(FeaturedProjects)