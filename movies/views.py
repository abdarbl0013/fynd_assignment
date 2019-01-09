from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.generics import CreateAPIView, ListAPIView, \
    RetrieveDestroyAPIView

from django_filters import rest_framework as filters

from utils.filters import MovieFilter
from utils.permissions import ReadOnly
from utils.mixins import PartialUpdateMixin

from .models import Movie
from .serializers import MovieSerializer


class MovieCreateView(CreateAPIView):
    """View to create Movie instance"""

    serializer_class = MovieSerializer
    permission_classes = (IsAdminUser,)


class MovieDetailsView(RetrieveDestroyAPIView, PartialUpdateMixin):
    """View to implement update, read and delete operation on Movie instance"""

    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    lookup_url_kwarg = 'movie_id'
    permission_classes = (IsAdminUser | ReadOnly,)


class MovieSearchView(ListAPIView):
    """View to search list of movies"""

    serializer_class = MovieSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Movie.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = MovieFilter
