from django.db import models
from accounts.models import CustomUser


class Expense_Type(models.Model):
    expense_name = models.CharField(max_length=80)

    def __str__(self):
        return self.expense_name


class Item(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item_name = models.CharField(max_length = 100)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    time_purchased = models.DateField(auto_now_add=True)
    expense_type = models.ForeignKey(Expense_Type,on_delete=models.SET_NULL,null=True)

    def __str__(self):   
        return f'{self.item_name} : {self.price}'