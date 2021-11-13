from django.test import TestCase
from spodaily_api.models import User, Contact


class UserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.test",
            password="testtesttest"
        )

    def test_user_creation(self):
        user = self.user
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.get_email(), user.email)
        self.assertEqual(user.get_password(), user.password)


class ContactTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.test",
            password="testtesttest"
        )

        self.contact = Contact.objects.create(
            user=self.user,
            reason='Bug',
            content='Test'
        )


    def test_contact_creation(self):
        contact = self.contact
        self.assertTrue(isinstance(contact, Contact))
        self.assertEqual(contact.get_user(), self.user)
