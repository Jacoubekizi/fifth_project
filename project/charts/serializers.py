from rest_framework import serializers
from .models import *
from accounts.methodes import *
import calendar
from django.db.models import Sum

class GroupedItemSerializer(serializers.Serializer):
    expense_type = serializers.CharField(source='expense_type__expense_name')
    sum = serializers.IntegerField()


class ItemsPerMonthSerializer(serializers.Serializer):
    month_name = serializers.SerializerMethodField()
    sum = serializers.IntegerField()

    def get_month_name(self, obj):
        return calendar.month_name[obj['month']]
    
class ItemSerializer(serializers.ModelSerializer):

    total_price = serializers.SerializerMethodField(read_only=True)
    user = serializers.CharField(source='client.username', read_only=True)
    expense_name = serializers.CharField(source='expense_type.expense_name', read_only=True)

    class Meta:
        model = Item
        exclude = ['client', 'expense_type']

    def get_total_price(self, obj):
        date = timezone.now().today()
        return Item.objects.filter(time_purchased__date=date).\
            aggregate(total_price=Sum('price'))['total_price'] or 0
        