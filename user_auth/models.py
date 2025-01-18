from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

USER_TYPE = (
    ('Vendor', 'Vendor'),
    ('Customer', 'Customer'),
)


class User(AbstractUser):
    username = models.CharField(max_length=200, null=True, blank=True)
    email = models.EmailField(unique=True)

    # Replacing the username with email while logging in .
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email 
    
    # Saving all the User fields to the database
    def save(self , *args, **kwargs):
        email_username,_ = self.email.split('@')
        if not self.username:
            self.username = email_username 
        super(User, self).save(*args,**kwargs)


class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images' , default='default-user.jpg', blank=True, null=True)
    fullname = models.CharField(max_length=200 , blank=True, null=True)
    mobile = models.CharField(max_length=200 , blank=True, null=True)
    user_Type= models.CharField(max_length=200 , choices =USER_TYPE, default=None , blank=True, null=True)

    def __str__(self):
        return self.user.username

    def save(self , *args, **kwargs):
        if not self.fullname:
            self.fullname = self.user.username 
        super(Profile, self).save(*args,**kwargs)