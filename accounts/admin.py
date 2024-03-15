from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import *
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Register your models here.
class AdminCustomUser(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['id', 'email','username', 'is_staff']    
    ordering = ['-id']

    fieldsets = (
        (None, 
                {'fields':('email', 'password',)}
            ),
            ('User Information',
                {'fields':('username', 'first_name', 'last_name','image')}
            ),
            ('Permissions', 
                {'fields':('is_verified', 'is_staff', 'is_superuser', 'is_active', 'groups','user_permissions')}
            ),
            ('Registration', 
                {'fields':('date_joined', 'last_login',)}
        )
    )

    add_fieldsets = (
        (None, {'classes':('wide',),
            'fields':(
                'email' , 'username', 'password1', 'password2',
            ),}
            ),
    )
admin.site.register(CustomUser, AdminCustomUser)
admin.site.register(CodeVerification)
admin.site.register(Account)
admin.site.register(AccountType)
