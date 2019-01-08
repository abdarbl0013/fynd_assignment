from rest_framework.permissions import IsAdminUser
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveUpdateDestroyAPIView

from django_filters import rest_framework as filters

from .models import Movie
from .filters import MovieFilter
from .permissions import ReadOnly
from .serializers import MovieSerializer


class MovieCreateView(CreateAPIView):
    """View to create Movie instance"""

    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)


class MovieDetailsView(RetrieveUpdateDestroyAPIView):
    """View to implement update, read and delete operation on Movie instance"""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_url_kwarg = 'movie_id'
    permission_classes = (IsAdminUser | ReadOnly,)


class MovieSearchView(ListAPIView):
    """View to search list of movies"""

    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
