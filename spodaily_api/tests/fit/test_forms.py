from django.test import TestCase
from spodaily_api.models import Session, User, Exercise
from spodaily_api.forms import LoginForm, CreateUserForm, EditUserForm, AddSessionForm, AddActivityForm, AddContactForm, \
    AddSessionProgramForm, AddSessionDuplicateForm


class LoginFormTest(TestCase):

    def test_email_is_invalid(self):
        form = LoginForm(data={"email": "test", "password": "password"})
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        form = LoginForm(data={"email": "test@test.test", "password": "password"})
        self.assertTrue(form.is_valid())


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


class AddSessionFormTest(TestCase):

    def test_date_is_invalid(self):
        form = AddSessionForm(data={"name": "name", "date": "test"})
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        form = AddSessionForm(data={"name": "name", "date": "2021-01-01"})
        self.assertTrue(form.is_valid())


class AddActivityFormTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name="test")
        self.exercise = Exercise.objects.create(name='test')

    def test_exercise_id_is_invalid(self):
        form = AddActivityForm(
            data={"session_id": self.session,
                  "exercise_id": 12,
                  "sets": 0,
                  "repetition": 0,
                  "rest": 0,
                  "weight": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_sets_is_invalid(self):
        form = AddActivityForm(
            data={"session_id": self.session,
                  "exercise_id": self.exercise,
                  "sets": 'test',
                  "repetition": 0,
                  "rest": 0,
                  "weight": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_repetition_is_invalid(self):
        form = AddActivityForm(
            data={"session_id": self.session,
                  "exercise_id": self.exercise,
                  "sets": 0,
                  "repetition": 'test',
                  "rest": 0,
                  "weight": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_rest_is_invalid(self):
        form = AddActivityForm(
            data={"session_id": self.session,
                  "exercise_id": self.exercise,
                  "sets": 0,
                  "repetition": 0,
                  "rest": 'test',
                  "weight": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_weight_is_invalid(self):
        form = AddActivityForm(
            data={"session_id": self.session,
                  "exercise_id": self.exercise,
                  "sets": 0,
                  "repetition": 0,
                  "rest": 0,
                  "weight": 'test',
            }
        )
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        form = AddActivityForm(
            data={"session_id": self.session,
                  "exercise_id": self.exercise,
                  "sets": 0,
                  "repetition": 0,
                  "rest": 12,
                  "weight": 0
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


class AddSessionProgramFormTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_is_valid(self):
        form = AddSessionProgramForm(
            data={"name": 'test'
            }
        )
        self.assertTrue(form.is_valid())


class AddSessionDuplicateFormTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_date_is_invalid(self):
        form = AddSessionDuplicateForm(
            data={"date": 'test'
                  }
        )
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        form = AddSessionDuplicateForm(
            data={"date": '2021-01-01'
                  }
        )
        self.assertTrue(form.is_valid())