from django_filters import rest_framework as filters

from movies.models import Movie


class MovieFilter(filters.FilterSet):
    """class defines filters for Movie

    Filters
    -------
    name : Allows filtering movies based on if string in movie name

    director : Allows filtering movies based on if string in movie's
    director name

    genre : filter movies based on if string matches (case insensitive)
    any of movie genres

    min_99popularity : filter movies where movie popularity is greater than or
     equal to value

    max_99popularity : filter movies where movie popularity is lower than or
     equal to value

    min_imdb_score : filter movies where movie imdb score is greater than or
     equal to value

    max_imdb_score : filter movies where movie imdb score is lower than or
     equal to value
    """

    name = filters.CharFilter(field_name='name', lookup_expr='icontains')
    director = filters.CharFilter(field_name='director',
                                  lookup_expr='icontains')
    genre = filters.CharFilter(field_name='genres__genre_name',
                               lookup_expr='iexact')
    min_99popularity = filters.NumberFilter(field_name='popularity',
                                            lookup_expr='gte')
    max_99popularity = filters.NumberFilter(field_name='popularity',
                                            lookup_expr='lte')
    min_imdb_score = filters.NumberFilter(field_name='imdb_score',
                                          lookup_expr='gte')
    max_imdb_score = filters.NumberFilter(field_name='imdb_score',
                                          lookup_expr='lte')

    class Meta:
        model = Movie
        fields = ['name', 'director', 'genre', 'max_99popularity',
                  'min_99popularity', 'max_imdb_score', 'min_imdb_score']
