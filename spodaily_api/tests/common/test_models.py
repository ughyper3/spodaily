from django.test import TestCase
from spodaily_api.models import User, Contact


class UserTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.test",
            password="testtesttest",
            accept_email=False
        )
        self.user2 = User.objects.create(
            email="test@test.test2",
            password="testtesttest2"
        )

    def test_user_creation(self):
        user = self.user
        user2 = self.user2
        self.assertTrue(isinstance(user, User))
        self.assertEqual(user.accept_email, False)
        self.assertEqual(user2.accept_email, True)
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
