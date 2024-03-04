from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from .methodes import *

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    phonenumber = PhoneNumberField(region='SY',unique=True)
    username = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/users', null=True,default='images/account.jpg')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',) 


    def __str__(self):
        return self.username
    
class CodeVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_time)

    def __str__(self):
        return f'{self.user.username} code:{self.code}'