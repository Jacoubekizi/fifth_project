from rest_framework import serializers
from .models import *
from accounts.methodes import *
import calendar


class GroupedItemSerializer(serializers.Serializer):
    expense_type = serializers.CharField(source='expense_type__expense_name')
    sum = serializers.IntegerField()



class ItemsPerMonthSerializer(serializers.Serializer):
    month_name = serializers.SerializerMethodField()
    sum = serializers.IntegerField()

    def get_month_name(self, obj):
        return calendar.month_name[obj['month']]