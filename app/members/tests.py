from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from members.models import Profile

User = get_user_model()


class UserTestCase(APITestCase):
    url = '/api/users'

    def setUp(self) -> None:
        self.user = User(
            email='test@test.com',
            password='1111'
        )
        self.user.set_password(self.user.password)
        self.user.save()
        self.user2 = User.objects.create_user(
            email='test2@test.com',
            password='1111'
        )

        self.profile = Profile.objects.create(
            user=self.user,
            username='testUser'
        )
        self.profile2 = Profile.objects.create(
            user=self.user2,
            username='testUser'
        )

    def test_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            'email': 'create@user.com',
            'password': '1111',
            'username': 'testUser'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.data
        self.assertEqual(response_data['email'], data['email'])

    def test_retrieve(self):
        url = self.url + f'/{self.user.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['id'], self.user.id)

    def test_partial_update(self):
        data = {
            'password:1111'
        }
        url = self.url + f'/{self.user.id}'
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user.email)
        self.assertEqual(response.data['id'], self.user.id)

    def test_destroy(self):
        url = self.url + f'/{self.user.id}'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_login(self):
        # login success > generating token
        data = {
            'email': self.user.email,
            'password': '1111'
        }
        url = self.url + '/login'
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['token'])

        # bad request
        data = {
            'email': self.user.email,
            'password': 'wrongPW'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # 401 != 400 request

        # login success > getting token
        data = {
            'email': self.user.email,
            'password': '1111'
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])

    def test_logout(self):
        self.client.force_authenticate(self.user)
        token = Token.objects.create(user=self.user)
        url = self.url + '/logout'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNone(token.key)

        self.assertEqual(Token.objects.filter(user=self.user).first(), None)

    def test_profile_retrieve(self):
        # 특정 계정의 프로필 조회
        self.client.force_authenticate(self.user)
        url = self.url + f'/{self.user.id}/profile/{self.profile.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 자기 자신의 프로필 조회
        self.client.force_authenticate(self.user2)
        url = self.url + f'/{self.user2.id}/profile'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        url = self.url + f'/{self.user.id}/change-password'
        self.client.force_authenticate(self.user)
        # password correct
        data = {
            'old_password': '1111',
            'new_password': '2222',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # password incorrect
        data = {
            'old_password': '11111',
            'new_password': '2222',
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
