from django.db import models
from taggit.managers import TaggableManager
from authentication.models import User
from django.contrib.auth import get_user_model
from django.db.models import Avg
# Category Class ------------------------> 

def get_current_user():
    """returns the current user id
        who is logged in and who is creating the project
    """
    return get_user_model().objects.get(id=1).id
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(default='Help others by donating to their fundraiser, or start one for someone you care about.')
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)

    def __str__(self):
        return self.name

# Projects Class ------------------------>
    
class Project(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('done', 'Done'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user, related_name='projects')
    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateField()
    end_time = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    tags = TaggableManager()
    image = models.ImageField(null=True,blank=True,upload_to='project_images/')
    featured = models.BooleanField(default=False)

    @classmethod
    def get_all_projects(cls):
        return cls.objects.all()

    @classmethod
    def get_project_by_id(cls, project_id):
        return cls.objects.get(id=project_id)
    
    @classmethod
    def get_top_rated_projects(cls):
        top_rated_projects = cls.objects.annotate(avg_rating=Avg('project_ratings__rating')).order_by('-avg_rating')
        return top_rated_projects

    def __str__(self):
        return self.title

class ProjectPicture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_images/')


    def __str__(self):
        return self.name


class Comments(models.Model):
    """
        in future will replace user_id with user model
        so we can show user name and profile picture in comments
        at the front end
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', default=get_current_user)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    
    @classmethod
    def get_comments_by_project(cls, project_id):
        """returns all comments for a project

        Args:
            project_id 
        Returns:
            list of comments related to the project as a queryset
        """
        return cls.objects.filter(project=project_id)
    
    
class ProjectsReports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reports', default=get_current_user)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_reports')
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report
    
class CommentsReports(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_reports', default=get_current_user)
    comment = models.ForeignKey(Comments, on_delete=models.CASCADE, related_name='comment_reports')
    report = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.report


class Donations(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations', default=get_current_user)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)
    
    @classmethod
    def get_sum_of_donations(cls, project_id):
        
        return cls.objects.filter(project=project_id).aggregate(models.Sum('amount'))['amount__sum']
    
    
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', default=get_current_user)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_ratings')
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
    
    @classmethod
    def get_avg_rating(cls, project_id):
        return cls.objects.filter(project=project_id).aggregate(models.Avg('rating'))['rating__avg']
    

