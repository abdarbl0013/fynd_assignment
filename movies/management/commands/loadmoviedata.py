import json
from os.path import isfile, join, isabs

from django.conf import settings
from django.core.management.base import BaseCommand

from movies.models import Movie, Genre


class Command(BaseCommand):
    """Command stores movie data from fixtures"""

    help = 'Loads movie data from fixtures into DB'

    def add_arguments(self, parser):
        """Adds positional and optional arguments to Command

        Notes
        -----
        Add positional argument:
            filepath - file path of fixture to be loaded on DB
        """

        # positional arguments
        parser.add_argument('filepath', type=str)

    def handle(self, *args, **options):
        """Defines logic to load movies data in DB"""

        # If file_path is absolute, set fixture_path to file_path
        # else, append file_path to base directory of project and
        # set as fixture_path
        file_path = options['filepath']
        fixture_path = file_path if isabs(file_path) else join(
            settings.BASE_DIR, file_path)

        # Validates file path provided, check if it points to actual file
        if not isfile(fixture_path):
            raise Exception('Invalid filepath')

        with open(fixture_path, 'r') as file_obj:
            data = json.load(file_obj)
            record_dict = dict()

            for movie_item in data:
                # Map movie item from data list to record dict
                # and create Movie record
                record_dict['name'] = movie_item.get('name')
                record_dict['popularity'] = movie_item.get('99popularity')
                record_dict['director'] = movie_item.get('director')
                record_dict['imdb_score'] = movie_item.get('imdb_score')
                movie, created = Movie.objects.get_or_create(**record_dict)

                genre_list = movie_item.get('genre')
                # create genre for each genre in list
                # and associate to current movie
                for genre in genre_list:
                    genre_obj, created = Genre.objects.get_or_create(
                        genre_name=genre.strip())
                    movie.genres.add(genre_obj)
                movie.save()

                self.stdout.write(str(movie))
