from django_filters import rest_framework as filters

from .models import Movie


class MovieFilter(filters.FilterSet):
    """class defines filters for Movie"""

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    director = filters.CharFilter(field_name='director',
                                  lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genres__genre_name',
                               lookup_expr='iexact')
    popularity = filters.NumberFilter(field_name='popularity',
                                      lookup_expr='gte')
    imdb_score = filters.NumberFilter(field_name='imdb_score',
                                      lookup_expr='gte')

    class Meta:
        model = Movie
        fields = ['name', 'director', 'genre', 'popularity', 'imdb_score']
