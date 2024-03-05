from rest_framework.views import APIView
from .serializers import *
from .models import Item , Expense_Type
from rest_framework.response import Response
from accounts.methodes import *
from django.db.models import Sum , F
from django.db.models.functions import ExtractMonth
from accounts.api.permissions import IsVerified
from rest_framework.permissions import IsAuthenticated

class PieChart(APIView): 
    permission_classes = (IsAuthenticated,)
    def get(self,request,year):
        client = CustomUser.objects.get(id=request.user.id)
        grouped_expenses = client.item_set.filter(time_purchased__year=year)\
                                        .values("expense_type__expense_name")\
                                        .annotate(sum=Sum("price"))\
                                        .values("expense_type__expense_name","sum").distinct()
        serializer = GroupedItemSerializer(grouped_expenses, many=True)
        return Response(serializer.data)


class LineChart(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,request, year):
        client = CustomUser.objects.get(id=request.user.id)
        grouped_expenses = client.item_set.filter(time_purchased__year=year).\
                                        annotate(item_price=F("price")).\
                                        annotate(month=ExtractMonth("time_purchased")).\
                                        values("month").annotate(sum=Sum("price")).\
                                        values("month", "sum").order_by("month")
        serializer = ItemsPerMonthSerializer(grouped_expenses, many=True)
        return Response(serializer.data)