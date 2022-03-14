from django.db import models
from django.core.validators import MinLengthValidator
from django.utils import timezone

# Create your models here.
class NseData(models.Model):
    nse_comp = models.CharField(max_length=200,default="")
    s_d = models.DateField(auto_now=False,blank=True,null=True)
    e_d = models.DateField(auto_now=False,blank=True,null=True)
    open_img = models.ImageField(upload_to="media/", max_length=250, default="")
    Change_img = models.ImageField(upload_to="media/", max_length=250, default="")
    Data_img = models.ImageField(upload_to="media/", max_length=250, default="")
    
    def __str__(self):
        return self.nse_comp
                                               

class UserDetails(models.Model):
    user_name = models.CharField(default="", max_length= 100)
    user_email = models.EmailField(unique = True)
    password = models.CharField(max_length = 50, validators=[MinLengthValidator(8)])
    last_login = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.user_email