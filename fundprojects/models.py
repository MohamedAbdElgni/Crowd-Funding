from django.db import models

# Create your models here.

# Category Class ------------------------> 

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

    title = models.CharField(max_length=100)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    # user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    user_id=models.IntegerField()
    picture = models.ForeignKey('ProjectPicture', on_delete=models.CASCADE, null=True, blank=True, related_name='project_pictures')
    tag = models.ForeignKey('Tag', on_delete=models.CASCADE, null=True, blank=True, related_name='project_tags')

    @classmethod
    def get_all_projects(cls):
        return cls.objects.all()

    @classmethod
    def get_project_by_id(cls, project_id):
        return cls.objects.get(id=project_id)

    def __str__(self):
        return self.title

class ProjectPicture(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_pictures')
    image = models.ImageField(upload_to='project_images/')

class Tag(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_tags')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name