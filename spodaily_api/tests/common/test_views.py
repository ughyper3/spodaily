from html import escape

from django.core import mail
from django.test import TestCase
from spodaily_api.views import *


class LoginTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_login_view(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_redirection(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('home'))
        self.failUnlessEqual(response.status_code, 200)
        self.client.logout()


class RegisterTest(TestCase):

    def test_register_view(self):
        url = reverse('register')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_redirection(self):
        response = self.client.post(reverse('register'),
                                    data={'email': 'test@example.com',
                                          'password1': 'testtesttest',
                                          'password2': 'testtesttest'})
        self.assertRedirects(response, reverse('register_success'))
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(User.objects.get(email='test@example.com').is_active, False)
        self.assertEqual(mail.outbox[0].subject, 'Activez votre compte Spodaily')
        self.assertTrue('http://testserver/activate/' in mail.outbox[0].body)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.count(), 1)


class RegisterSuccessTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_login_view(self):
        url = reverse('register_success')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register_success.html')

    def test_login_redirection(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('register_success'))
        self.failUnlessEqual(response.status_code, 200)
        self.client.logout()


class AccountTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_account_not_authenticated_user(self):
        url = reverse('account')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/account.html')
        self.assertEqual(response.status_code, 302)

    def test_account_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('account'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/account.html')
        self.client.logout()


class LogoutTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_logout_not_authenticated_user(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/logged_out.html')
        self.assertEqual(response.status_code, 200)

    def test_logout_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html')
        self.client.logout()


class AddContactTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_contact_not_authenticated_user(self):
        url = reverse('contact')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/contact.html')
        self.assertEqual(response.status_code, 302)

    def test_contact_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/contact.html')
        self.client.logout()


class RulesOfUseTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_rules_of_use_not_authenticated_user(self):
        url = reverse('rules_of_use')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/rules_of_use.html')
        self.assertEqual(response.status_code, 302)

    def test_rules_of_use_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('rules_of_use'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/rules_of_use.html')
        self.client.logout()


class CGUTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_rules_of_use_not_authenticated_user(self):
        url = reverse('cgu')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'registration/cgu.html')
        self.assertEqual(response.status_code, 200)

    def test_rules_of_use_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('cgu'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/cgu.html')
        self.client.logout()


class DeleteAccountView(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_delete_account_not_authenticated_user(self):
        url = reverse('delete_account', args=[self.pascal.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/delete_account.html')
        self.assertEqual(response.status_code, 302)

    def test_rules_of_use_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('delete_account', args=[self.pascal.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/delete_account.html')
        self.client.logout()


