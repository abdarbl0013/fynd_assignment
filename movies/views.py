from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveDestroyAPIView

from django_filters import rest_framework as filters

from utils.filters import MovieFilter
from utils.permissions import ReadOnlyAuthenticated
from utils.mixins import PartialUpdateMixin

from .models import Movie
from .serializers import MovieSerializer


class MovieCreateView(CreateAPIView):
    """View to create Movie instance

    Notes
    -----
    only Admin (staff member) user are allowed to create Movie instance.
    """

    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)


class MovieDetailsView(RetrieveDestroyAPIView, PartialUpdateMixin):
    """View to implement update, read and delete operation on Movie instance

    Notes
    -----
    Only Admin user can modify movie instance. All authenticated user
     has read access.
    """

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_url_kwarg = 'movie_id'
    permission_classes = (IsAdminUser | ReadOnlyAuthenticated,)


class MovieSearchView(ListAPIView):
    """View to search list of movies

    Notes
    -----
    Only Authenticated user can search for movies.

    Pass values in query parameters to search
    Movies can be search based on:
            name, director, genre,
            max_imdb_score, min_imdb_score, max_99popularity, min_99popularity
    """

    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Movie.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
