from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from .methodes import *


class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True,null=True,blank=True)
    username = models.CharField(max_length=200)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(upload_to='images/users', null=True,default='images/account.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username',)

    def __str__(self):
        return self.username
    


class AccountType(models.Model):
    name = models.CharField(max_length=50)

    def __atr__(self) -> str:
        return self.name




class Account(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    currency = models.CharField(max_length=20)
    account_type = models.ForeignKey(AccountType,on_delete=models.CASCADE)
    notes = models.TextField()
    budget = models.FloatField()

    def __str__(self) -> str:
        return f'{self.user.username}-{self.account_type}'





class CodeVerification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    code = models.IntegerField(validators=[MinValueValidator(1000), MaxValueValidator(9999)])
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=get_expiration_time)

    def __str__(self):
        return f'{self.user.username} code:{self.code}'
    



