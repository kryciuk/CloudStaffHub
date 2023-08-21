from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status


class TestCandidateUrls(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client(HTTP_HOST='localhost:8000')

        user = User.objects.create(username='test_user1', email='test_user1@test.com')
        user.set_password('password')
        user.save()

        cls.user = user

    def test_url_exists_at_correct_location(self):
        user_login = self.client.login(username=self.user.username, password='password')
        response = self.client.get('/candidate/', {'user_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_available_by_name(self):
        user_login = self.client.login(username=self.user.username, password='password')
        response = self.client.get(reverse('candidate-dashboard'), {'user_id': self.user.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('candidate-dashboard'))
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
