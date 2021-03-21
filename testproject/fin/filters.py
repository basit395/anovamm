import django_filters
from .models import textstream






class textstreamFilter(django_filters.FilterSet):
    mytext = django_filters.CharFilter(lookup_expr='icontains')
    class Meta:
        model = textstream
        fields = ['mytext','impression']
