from django.test import TestCase
from django.urls import reverse
from spodaily_api.models import User


class HomeTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_home_not_authenticated_user(self):
        url = reverse('food_home')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/food/home.html')
        self.assertEqual(response.status_code, 302)

    def test_home_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('food_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/food/home.html')
        self.client.logout()