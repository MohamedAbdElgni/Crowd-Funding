from django.db import models

# Create your models here.
from django.db import models
class Register(models.Model):
    first_name = models.CharField(max_length = 30, null=False, blank=False)
    last_name = models.CharField(max_length = 30,null=False)
    email = models.EmailField(max_length = 50 , unique=True,null=False)
    password = models.CharField(max_length = 200,null=False)
    phone = models.CharField(max_length = 11 , unique=True, null=False)
    is_active = models.BooleanField(default=False)
    # profile_img = models.ImageField(verbose_name="photo", upload_to='user/images/' ,default='default.jpg')
 
    def __str__(self):
        fullName= f""+(self.first_name + " " +self.last_name) 
        return fullName
