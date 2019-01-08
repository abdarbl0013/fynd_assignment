from rest_framework import serializers

from .models import Movie, Genre
from .custom_fields import GetOrCreatePrimaryKeyRelatedField


class MovieSerializer(serializers.ModelSerializer):
    """Serialize / deserialize Movie data"""

    genre = GetOrCreatePrimaryKeyRelatedField(
        queryset=Genre.objects.all(), many=True,
        source='genres', required=False, model=Genre,
        pk_field=serializers.CharField(max_length=20, trim_whitespace=True)
    )

    class Meta:
        """Meta class fot MovieSerializer"""

        model = Movie
        fields = ('id', 'name', 'director', 'imdb_score', '99popularity',
                  'genre')
        read_only_fields = ('id',)
        extra_kwargs = {
            '99popularity': {'source': 'popularity'}
        }

    def add_movie_genres(self, movie_obj, genre_list):
        """Associates list of genre objects to movie obj"""

        for genre in genre_list:
            movie_obj.genres.add(genre)
        movie_obj.save()

    def create(self, validated_data):
        """Override 'create' method to enable writing to M2M related field

        Notes
        -----
        Pop genre list from validated data before creating Movie instance.
        Call 'add_movie_genres' to associate list of genre objects to movie obj
        """

        # Create movie instance after popping genre list from dict
        genre_list = validated_data.pop('genres', list())
        movie_obj = Movie.objects.create(**validated_data)

        self.add_movie_genres(movie_obj, genre_list)

        return movie_obj

    def update(self, instance, validated_data):
        """Override 'update' method to enable writing to M2M related field"""

        for attr, value in validated_data.items():
            # If attribute 'genres' in dict items,
            # call 'add_movie_genres' to associate genres to instance
            if attr == 'genres':
                self.add_movie_genres(instance, value)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance
