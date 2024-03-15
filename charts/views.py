from rest_framework.views import APIView
from .serializers import *
from .models import Item 
from rest_framework.response import Response
from accounts.methodes import *
from django.db.models import Sum , F , Q
from django.db.models.functions import ExtractMonth
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView , GenericAPIView , RetrieveUpdateDestroyAPIView
from project.filters import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status


class Items(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = CustomUser.objects.get(id=self.request.user.id)
        category = ExpenseCategory.objects.get(name=self.request.data['name'])
        serializer.save(client=user, category=category)



class ListCreateCategory(ListCreateAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend]



class RetUpdDesCategory(RetrieveUpdateDestroyAPIView):
    queryset = ExpenseCategory.objects.all()
    serializer_class = CategorySerializer




class ListCreateSubCategory(ListCreateAPIView):
    queryset = ExpenseSubCategory.objects.all()
    serializer_class = SubCategorySerializer
    filter_backends = [DjangoFilterBackend]




class RetUpdDesSubCategory(RetrieveUpdateDestroyAPIView):
    queryset = ExpenseSubCategory.objects.all()
    serializer_class = SubCategorySerializer




class ListCreateUpcomingPayment(ListCreateAPIView):
    queryset = UpcomingPayment.objects.all()
    serializer_class = UpcomingPaymentSerializer



class RetUpdDesUpcomingPayment(RetrieveUpdateDestroyAPIView):
    queryset = UpcomingPayment.objects.all()
    serializer_class = UpcomingPaymentSerializer



class PieChartCategories(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter

    def get(self,request,account_id):
        account = Account.objects.get(id=account_id)
        if request.user != account.user:
            return Response({"error" : "you are not allowed in this account"} ,status=status.HTTP_403_FORBIDDEN)
        queryset = self.filter_queryset(Item.objects.filter(account=account_id))
        grouped_expenses = queryset.values("subcategory__category__name")\
                                    .annotate(sum=Sum("price"))\
                                    .values("subcategory__category__name","sum").distinct()
        serializer = GroupCategoriesSerializer(grouped_expenses, many=True)
        return Response(serializer.data)



class PieChartSubCategory(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = ItemFilter

    def post(self,request,account_id):
        category = request.data['category']
        account = Account.objects.get(id=account_id)
        if request.user != account.user:
            return Response({"error" : "you are not allowed in this account"} ,status=status.HTTP_403_FORBIDDEN)
        
        queryset = self.filter_queryset(Item.objects.filter(Q(user=request.user)&Q(subcategory__category__name=category)))
        grouped_expenses = queryset.values("subcategory__category__name")\
                                    .annotate(sum=Sum("price"))\
                                    .values("subcategory__category__name","sum").distinct()
        serializer = GroupCategoriesSerializer(grouped_expenses, many=True)
        return Response(serializer.data)



class LineChart(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self,request, year):
        grouped_expenses = Item.objects.filter(Q(created=year)&Q(user=self.request.user)).\
                                        annotate(item_price=F("price")).\
                                        annotate(month=ExtractMonth("created")).\
                                        values("month").annotate(sum=Sum("price")).\
                                        values("month", "sum").order_by("month")
        serializer = ItemsPerMonthSerializer(grouped_expenses, many=True)
        return Response(serializer.data)




class CreateItem(ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        user = CustomUser.objects.get(id=self.request.user.id)
        category = ExpenseCategory.objects.get(name=self.request.data['name'])
        serializer.save(client=user, category=category)

    def get_queryset(self):
        date = timezone.now().today()
        return Item.objects.filter(created__date=date)