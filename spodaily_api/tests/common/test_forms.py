from django.test import TestCase
from spodaily_api.forms import CreateUserForm, EditUserForm, AddContactForm
from spodaily_api.models import User


class CreateUserFormTest(TestCase):

    def test_email_is_invalid(self):
        form = CreateUserForm(data={"email": "test", "password1": "password", "password2": "password"})
        self.assertFalse(form.is_valid())

    def test_password_is_invalid(self):
        form = CreateUserForm(data={"email": "test@test.test", "password1": "password", "password2": "passwordd"})
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        form = CreateUserForm(data={"email": "test@test.test", "password1": "adminpassword", "password2": "adminpassword"})
        self.assertTrue(form.is_valid())


class EditUserFormTest(TestCase):

    def test_email_is_invalid(self):
        form = EditUserForm(
            data={"email": "test",
                  "name": "test",
                  "first_name": "test",
                  "birth": "2021-01-01",
                  "height": 180,
                  "weight": 80,
                  "sexe": "Autre"
            }
        )
        self.assertFalse(form.is_valid())

    def test_birth_is_invalid(self):
        form = EditUserForm(
            data={"email": "test@test.test",
                  "name": "test",
                  "first_name": "test",
                  "birth": "test",
                  "height": 180,
                  "weight": 80,
                  "sexe": "Autre"
                  }
        )
        self.assertFalse(form.is_valid())

    def test_height_is_invalid(self):
        form = EditUserForm(
            data={"email": "test@test.test",
                  "name": "test",
                  "first_name": "test",
                  "birth": "2021-01-01",
                  "height": "test",
                  "weight": 80,
                  "sexe": "Autre"
                  }
        )
        self.assertFalse(form.is_valid())

    def test_weight_is_invalid(self):
        form = EditUserForm(
            data={"email": "test@test.test",
                  "name": "test",
                  "first_name": "test",
                  "birth": "2021-01-01",
                  "height": 180,
                  "weight": "test",
                  "sexe": "Autre"
                  }
        )
        self.assertFalse(form.is_valid())

    def test_sexe_is_invalid(self):
        form = EditUserForm(
            data={"email": "test@test.test",
                  "name": "test",
                  "first_name": "test",
                  "birth": "2021-01-01",
                  "height": 180,
                  "weight": 80,
                  "sexe": "Mixeur"
                  }
        )
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        form = EditUserForm(
            data={"email": "test@test.test",
                  "name": "test",
                  "first_name": "test",
                  "birth": "2021-01-01",
                  "height": 180,
                  "weight": 80,
                  "sexe": "Autre"
            }
        )
        self.assertTrue(form.is_valid())


class AddContactFormTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_reason_is_invalid(self):
        form = AddContactForm(
            data={"reason": 'test',
                  "content": 'test'
            }
        )
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        form = AddContactForm(
            data={"reason": 'Bug',
                  "content": 'test'
            }
        )
        self.assertTrue(form.is_valid())