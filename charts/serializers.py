from rest_framework import serializers
from .models import *
from accounts.methodes import *
import calendar



class ItemsPerMonthSerializer(serializers.Serializer):
    month_name = serializers.SerializerMethodField()
    sum = serializers.IntegerField()

    def get_month_name(self, obj):
        return calendar.month_name[obj['month']]
    


class GroupCategoriesSerializer(serializers.Serializer):
    category = serializers.CharField(source='subcategory__category__name')
    sum = serializers.IntegerField()



class GroupSubCategoriesSerializer(serializers.Serializer):
    subcategory = serializers.CharField(source='subcategory__name')
    sum = serializers.IntegerField()



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseCategory
        fields = '__all__'



class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSubCategory
        fields = '__all__'



class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'




class UpcomingPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UpcomingPayment
        fields = '__all__'        




