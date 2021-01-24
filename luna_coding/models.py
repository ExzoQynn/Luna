from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)
    photo_profile = models.ImageField(default='photo_profile/default_profile.png',upload_to='photo_profile',blank=True,null=True)
    user_type = models.CharField(max_length=100,null=True,blank=True,default='C')

    def __str__(self):
        return f'{self.user.username} Profile'