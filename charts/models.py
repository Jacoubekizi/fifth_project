from django.db import models



class Expense_Type(models.Model):
    expense_name = models.CharField(max_length=80)

    def __str__(self):
        return self.expense_name


class Item(models.Model):
    item_name = models.CharField(max_length = 100)
    price = models.IntegerField(default=0)
    time_purchased = models.DateTimeField(auto_now_add=True)
    expense_type = models.ForeignKey(Expense_Type,on_delete=models.SET_NULL,null=True)

    def __str__(self):   
        return f'{self.item_name} : {self.price}'