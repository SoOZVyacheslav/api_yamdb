from django_filters import rest_framework as filters
from django_filters.filters import CharFilter

from reviews.models import Title


class Filter(filters.FilterSet):
    year = CharFilter(field_name='year',)
    category = CharFilter(field_name='category__slug', lookup_expr='contains')
    genre = CharFilter(field_name='genre__slug', lookup_expr='contains')
    name = CharFilter(field_name='name', lookup_expr='contains')

    class Meta:
        model = Title
        fields = '__all__'
