from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from posts.models import Post, Comment

User = get_user_model()


class PostTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='testUser@test.com',
            password='1111'
        )

        for i in range(2):
            self.post = Post.objects.create(
                user=self.user,
                title=f'test Post {i}'
            )
        self.url = f'/api/users/{self.user.id}/posts'

    def test_list(self):
        self.client.force_authenticate(self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create(self):
        data = {
            'title': 'testPost',
            'content': 'test content',
        }
        self.client.force_authenticate(self.user)
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.fail()

    def test_retrieve(self):
        url = self.url + f'/{self.post.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.user.id, response.data['user'])
        self.assertEqual(self.post.title, response.data['title'])

    def test_update(self):
        url = self.url + f'/{self.post.id}'
        data = {
            'title': 'update title',
            'content': 'update content',
        }
        self.client.force_authenticate(self.user)
        response = self.client.patch(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.post.id, response.data['id'])
        self.assertEqual(data['title'], response.data['title'])
        self.assertEqual(data['content'], response.data['content'])

    def test_destroy(self):
        url = self.url + f'/{self.post.id}'
        self.client.force_authenticate(self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class CommentTest(APITestCase):
    def setUp(self) -> None:
        self.user = User.object.create_user(
            email='testUser@test.com',
            password='1111',
        )
        self.post = Post.objects.create(
            title='test Post title',
            content='test Content title',
        )
        self.comment = Comment.objects.create(
            content='test content',
            post=self.post,
            user=self.user,
        )

    def test_comment_list(self):
        self.fail()

    def tesT_create(self):
        data = {

        }
        self.fail()
