from django.test import TestCase
from spodaily_api.models import Session, User, Exercise
from spodaily_api.forms import LoginForm, CreateUserForm, EditUserForm, AddSessionForm, AddActivityForm, AddContactForm, \
    AddSessionProgramForm, AddSessionDuplicateForm, SessionDoneForm, SettingsProgramSessionForm


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


class AddSessionProgramFormTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_is_valid(self):
        form = AddSessionProgramForm(
            data={"name": 'test',
                  'recurrence': 7
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


class SessionDoneFormTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_is_valid(self):
        form = SessionDoneForm(
            data={"is_done": True
                  }
        )
        self.assertTrue(form.is_valid())


class SettingsProgramSessionFormTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_recurrence_is_invalid(self):
        form = SettingsProgramSessionForm(
            data={"recurrence": "test",
                  "name": "issou"
                  }
        )
        self.assertFalse(form.is_valid())

    def test_is_valid(self):
        form = SettingsProgramSessionForm(
            data={"recurrence": 7,
                  "name": "issou"
                  }
        )
        self.assertTrue(form.is_valid())