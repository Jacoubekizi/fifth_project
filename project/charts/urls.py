from django.urls import path
from .views import *

urlpatterns = [
    path('pie-chart/<str:year>' , PieChart.as_view()),
    path('line-chart/<str:year>' , LineChart.as_view()),
    path('create-item/', CreateItem.as_view()),
    path('ret-upd-des-item/<str:pk>/', RetUpdDesView.as_view()),
]