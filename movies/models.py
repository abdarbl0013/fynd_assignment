from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Genre(models.Model):
    """Movie genre model"""

    genre_name = models.CharField(max_length=20, primary_key=True)


class Movie(models.Model):
    """Model to store movie data"""

    name = models.CharField(max_length=255)
    director = models.CharField(max_length=50)
    imdb_score = models.FloatField(null=True, blank=True,
                                    validators=[MaxValueValidator(10.0),
                                                MinValueValidator(1.0)])
    popularity = models.PositiveIntegerField(null=True, blank=True,
                                             validators=[
                                                 MaxValueValidator(99)])
    genres = models.ManyToManyField(Genre, related_name='movies')

    class Meta:
        unique_together = ('name', 'director')
