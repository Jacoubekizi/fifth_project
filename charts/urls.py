from django.urls import path
from .views import *

urlpatterns = [
    path('pie-chart/<str:year>' , PieChart.as_view()),
    path('line-chart/<str:year>' , LineChart.as_view())
]