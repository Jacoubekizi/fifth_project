from django.contrib import admin
from .models import *

admin.site.register(ExpenseCategory)
admin.site.register(ExpenseSubCategory)
admin.site.register(Item)
admin.register(UpcomingPayment)
