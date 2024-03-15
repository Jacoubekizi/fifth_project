from django.urls import path
from .views import *

urlpatterns = [
    path('subcategories/' , ListCreateSubCategory.as_view()),
    path('get-subcategory/<str:pk>' , RetUpdDesSubCategory.as_view()),
    path('categories/' , ListCreateCategory.as_view()),
    path('get-category/<str:pk>' , RetUpdDesCategory.as_view()),
    path('upcoming-payments/' , ListCreateUpcomingPayment.as_view()),
    path('get-upcoming-payment/<str:pk>' ,RetUpdDesUpcomingPayment.as_view()),
    path('pie-categories/' , PieChartCategories.as_view()),
    path('pie-subcategories/' , PieChartSubCategory.as_view()),
    path('line-chart/<str:year>' , LineChart.as_view()),
    path('create-item/', CreateItem.as_view()),
    path('items/' , Items.as_view())
]