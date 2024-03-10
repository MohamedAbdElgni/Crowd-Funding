from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
# Create your models here.



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(validators=[RegexValidator('^01[0-2,5]{1}[0-9]{8}$')], max_length=11, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, default='profile_pics/default.jpg')
    birth_date = models.DateField(null=True, blank=True)
    facebook = models.URLField(max_length=200, blank=True)
    twitter = models.URLField(max_length=200, blank=True)
    linkedin = models.URLField(max_length=200, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'