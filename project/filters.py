import django_filters
from accounts.models import *
from charts.models import *


class ItemFilter(django_filters.FilterSet):
    date_from = django_filters.DateFilter(field_name='created', lookup_expr='gte')
    date_to = django_filters.DateFilter(field_name='created', lookup_expr='lte')
    
    class Meta:
        model = Item
        fields = ['date_from', 'date_to']
