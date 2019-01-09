import json
import base64
from urllib.parse import urlencode
from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth.models import User

from .models import Movie, Genre


class MovieTestCase(TestCase):
    """Test cases for 'users' app"""

    def setUp(self):
        """Sets up sample placeholder values / environment for test cases"""

        self.client = APIClient()
        self.content_type = 'application/json'

        username = 'app_tester'
        password = 'abcd1234'
        self.user = User.objects.create_user(
            username=username,
            password=password,
            email='tester@gmail.com'
        )

        usr_pass = '%s:%s' % (username, password)
        b64val = base64.b64encode(bytes(usr_pass, 'utf-8')).decode("ascii")
        self.auth_header = 'Basic ' + b64val

        admin_username = 'admin_tester'
        admin_password = 'xyz01234'
        self.admin_user = User.objects.create_user(
            username=admin_username,
            password=admin_password,
            email='admin.tester@gmail.com',
            is_staff=True
        )

        usr_pass = '%s:%s' % (admin_username, admin_password)
        b64val = base64.b64encode(bytes(usr_pass, 'utf-8')).decode("ascii")
        self.admin_auth_header = 'Basic ' + b64val

        self.sample_movie = Movie.objects.create(name='Sample Movie Name',
                                                 director='Anon')

    def test_movie_create(self):
        """Test APi to create movie instance"""

        create_data = {
            "99popularity": 84.0,
            "director": "Stanley Donen",
            "genre": [
                "Comedy",
                " Musical",
                " Romance"
            ],
            "imdb_score": 8.4,
            "name": "Singin in the Rain"
        }
        url = '/movie/'
        response = self.client.post(url, json.dumps(create_data),
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.data
        self.assertEqual(response_data['detail'],
                         'Authentication credentials were not provided.')

        headers = {'HTTP_AUTHORIZATION': self.auth_header}
        response = self.client.post(url, json.dumps(create_data),
                                   content_type=self.content_type, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_data = response.data
        self.assertEqual(response_data['detail'],
                         'You do not have permission to perform this action.')

        headers = {'HTTP_AUTHORIZATION': self.admin_auth_header}
        response = self.client.post(url, json.dumps(create_data),
                                    content_type=self.content_type, **headers)
        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data

        movie = Movie.objects.get(id=response_data['id'])
        self.assertEqual(movie.name, create_data['name'])

        movie_genres = movie.genres.all()
        for genre_name in create_data['genre']:
            genre_qs = Genre.objects.filter(genre_name=genre_name.strip())
            self.assertEqual(len(genre_qs), 1)

            self.assertIn(genre_qs[0], movie_genres)

    def test_movie_update(self):
        """Test API to update movie instance"""

        update_data = {
            "genre": [],
            "imdb_score": 6.4,
        }

        url = '/movie/{0}/'.format(self.sample_movie.id)
        response = self.client.put(url, json.dumps(update_data),
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.data
        self.assertEqual(response_data['detail'],
                         'Authentication credentials were not provided.')

        headers = {'HTTP_AUTHORIZATION': self.auth_header}
        response = self.client.put(url, json.dumps(update_data),
                                    content_type=self.content_type, **headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response_data = response.data
        self.assertEqual(response_data['detail'],
                         'You do not have permission to perform this action.')

        headers = {'HTTP_AUTHORIZATION': self.admin_auth_header}
        response = self.client.put(url, json.dumps(update_data),
                                    content_type=self.content_type, **headers)
        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data

        movie = Movie.objects.get(id=self.sample_movie.id)
        self.assertEqual(movie.imdb_score, update_data['imdb_score'])

        movie_genres = movie.genres.all()
        self.assertFalse(len(movie_genres))

        update_data = {
            "genre": [
                "Drama",
                " Thriller "
            ]
        }
        response = self.client.put(url, json.dumps(update_data),
                                   content_type=self.content_type, **headers)

        movie = Movie.objects.get(id=self.sample_movie.id)
        movie_genres = movie.genres.all()
        for genre_name in update_data['genre']:
            genre_qs = Genre.objects.filter(genre_name=genre_name.strip())
            self.assertEqual(len(genre_qs), 1)

            self.assertIn(genre_qs[0], movie_genres)

    def test_movie_get(self):
        """Test API to read movie instance"""

        url = '/movie/{0}/'.format(self.sample_movie.id)

        response = self.client.get(url)
        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data
        self.assertEqual(self.sample_movie.name, response_data['name'])

    def test_movie_delete(self):
        """Test API to delete movie instance"""

        url = '/movie/{0}/'.format(self.sample_movie.id)
        headers = {'HTTP_AUTHORIZATION': self.admin_auth_header}

        response = self.client.delete(url, **headers)
        self.assertTrue(status.is_success(response.status_code))

        movies = Movie.objects.filter(id=self.sample_movie.id)
        self.assertFalse(len(movies))

    def test_movie_search(self):
        """Test API to search movies"""

        movie_list = [
            {
                "popularity": 84.0,
                "director": "Clyde Bruckman",
                "genres": [
                    "Comedy",
                    "Romance",
                    "War",
                    "Action"
                ],
                "imdb_score": 8.4,
                "name": "The General"
            },
            {
                "popularity": 78.0,
                "director": "Ivan Reitman",
                "genres": [
                    "Adventure",
                    "Fantasy",
                    "Mystery"
                ],
                "imdb_score": 7.8,
                "name": "Ghost Busters"
            },
            {
                "popularity": 71.0,
                "director": "Ivan Dyke",
                "genres": [
                    "Action",
                    "Adventure",
                    "Romance"
                ],
                "imdb_score": 7.1,
                "name": "Tarzan the Ape Man"
            },
        ]

        for movie_dict in movie_list:
            genres = movie_dict.pop('genres')
            movie = Movie.objects.create(**movie_dict)
            for genre_name in genres:
                genre_obj, created = Genre.objects.get_or_create(
                    genre_name=genre_name)
                movie.genres.add(genre_obj)
            movie.save()

        base_url = '/movie/search/'
        response = self.client.get(base_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.data
        self.assertEqual(response_data['detail'],
                         'Authentication credentials were not provided.')

        headers = {'HTTP_AUTHORIZATION': self.auth_header}
        params = {'name': 'the'}
        url = base_url + '?{}'.format(urlencode(params))

        response = self.client.get(url, **headers)
        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data
        self.assertEqual(len(response_data), 2)

        response_movie_names = [dct['name'] for dct in response_data]
        self.assertEqual(sorted(['Tarzan the Ape Man', 'The General']),
                         sorted(response_movie_names))

        params = {'director': 'ivan'}
        url = base_url + '?{}'.format(urlencode(params))

        response = self.client.get(url, **headers)
        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data
        self.assertEqual(len(response_data), 2)

        response_movie_names = [dct['name'] for dct in response_data]
        self.assertEqual(sorted(['Ghost Busters', 'Tarzan the Ape Man']),
                         sorted(response_movie_names))

        params = {'genre': 'romance'}
        url = base_url + '?{}'.format(urlencode(params))

        response = self.client.get(url, **headers)
        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data
        self.assertEqual(len(response_data), 2)

        response_movie_names = [dct['name'] for dct in response_data]
        self.assertEqual(sorted(['Tarzan the Ape Man', 'The General']),
                         sorted(response_movie_names))

        params = {'max_imdb_score': 8}
        url = base_url + '?{}'.format(urlencode(params))

        response = self.client.get(url, **headers)
        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data
        self.assertEqual(len(response_data), 2)

        response_movie_names = [dct['name'] for dct in response_data]
        self.assertEqual(sorted(['Ghost Busters', 'Tarzan the Ape Man']),
                         sorted(response_movie_names))
