import json
import base64
from rest_framework import status
from rest_framework.test import APIClient

from django.test import TestCase
from django.contrib.auth.models import User


class UserTestCase(TestCase):
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

    def test_user_register(self):
        """Test User registration"""

        create_data = {
            'first_name': 'Placeholder',
            'last_name': 'User',
            'email': 'placeholder@seynse.com',
            'username': 'placeholder_user',
            'password': 'efgh5678'
        }

        url = '/user/register/'
        response = self.client.post(url, json.dumps(create_data),
                                    content_type=self.content_type)
        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data

        users = User.objects.filter(username=create_data['username'])
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].id, response_data['id'])

    def test_user_update(self):
        """Test update operation on User"""

        update_data = {
            'email': 'tester1@seynse.com',
            'password': 'abcd1239'
        }

        url = '/user/details/'
        response = self.client.put(url, json.dumps(update_data),
                                   content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.data
        self.assertEqual(response_data['detail'],
                         'Authentication credentials were not provided.')

        headers = {'HTTP_AUTHORIZATION': self.auth_header}
        response = self.client.put(url, json.dumps(update_data),
                                   content_type=self.content_type, **headers)
        self.assertTrue(status.is_client_error(response.status_code))
        response_data = response.data
        self.assertEqual(response_data['non_field_errors'][0],
                         'Password update is not allowed')

        update_data = {
            'email': 'tester1@seynse.com'
        }
        response = self.client.put(url, json.dumps(update_data),
                                   content_type=self.content_type, **headers)
        self.assertTrue(status.is_success(response.status_code))

        user_obj = User.objects.get(id=self.user.id)
        self.assertEqual(user_obj.email, update_data['email'])

    def test_user_get(self):
        """Test read operation on User"""

        url = '/user/details/'
        headers = {'HTTP_AUTHORIZATION': self.auth_header}
        response = self.client.get(url, **headers)

        self.assertTrue(status.is_success(response.status_code))
        response_data = response.data
        self.assertNotIn('password', response_data.keys())
        self.assertEqual(self.user.id, response_data['id'])

    def test_user_delete(self):
        """Test delete operation on User"""

        url = '/user/details/'
        headers = {'HTTP_AUTHORIZATION': self.auth_header}
        response = self.client.delete(url, **headers)

        self.assertTrue(status.is_success(response.status_code))
        user_obj = User.objects.get(id=self.user.id)
        self.assertFalse(user_obj.is_active)

        response = self.client.get(url, **headers)
        self.assertTrue(status.is_client_error(response.status_code))
        response_data = response.data
        self.assertEqual(response_data['detail'], 'Invalid username/password.')

    def test_password_change(self):
        """Test API to change password"""

        url = '/user/change_password/'
        headers = {'HTTP_AUTHORIZATION': self.auth_header}
        data = {
            'old_password': 'abcd1234',
            'new_password': 'asdf9'
        }

        response = self.client.post(url, json.dumps(data),
                                    content_type=self.content_type)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response_data = response.data
        self.assertEqual(response_data['detail'],
                         'Authentication credentials were not provided.')

        response = self.client.post(url, json.dumps(data),
                                    content_type=self.content_type, **headers)
        self.assertTrue(status.is_client_error(response.status_code))
        response_data = response.data
        self.assertEqual(response_data['new_password'][0],
                         'Ensure this field has at least 8 characters.')

        data = {
            'old_password': 'abcd1235',
            'new_password': 'asdf9000'
        }

        response = self.client.post(url, json.dumps(data),
                                    content_type=self.content_type, **headers)
        self.assertTrue(status.is_client_error(response.status_code))
        response_data = response.data
        self.assertEqual(response_data['old_password'][0], 'Wrong password.')

        data['old_password'] = 'abcd1234'
        response = self.client.post(url, json.dumps(data),
                                    content_type=self.content_type, **headers)
        self.assertTrue(status.is_success(response.status_code))

        user_obj = User.objects.get(id=self.user.id)
        self.assertTrue(user_obj.check_password(data['new_password']))
