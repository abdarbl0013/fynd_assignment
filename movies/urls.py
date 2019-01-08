from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.MovieCreateView.as_view()),
    url(r'^(?P<movie_id>\d+)/$', views.MovieDetailsView.as_view()),
    url(r'^search/$', views.MovieSearchView.as_view())
]
