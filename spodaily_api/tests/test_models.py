from django.test import TestCase
from spodaily_api.models import Session, User, Exercise, Activity, Muscle


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


class SessionTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.test",
            password="testtesttest"
        )
        self.session = Session.objects.create(
            user=self.user,
            name='test'
        )

    def test_session_creation(self):
        session = self.session
        self.assertTrue(isinstance(session, Session))
        self.assertEqual(session.get_name(), session.name)
        self.assertEqual(session.get_user(), session.user)


class ExerciseTestCase(TestCase):

    def setUp(self):
        self.exercise = Exercise.objects.create(
            name="test"
        )

    def test_exercise_creation(self):
        exercise = self.exercise
        self.assertTrue(isinstance(exercise, Exercise))
        self.assertEqual(exercise.get_name(), exercise.name)


class ActivityTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.test",
            password="testtesttest"
        )
        self.session = Session.objects.create(
            user=self.user,
            name='test'
        )
        self.exercise = Exercise.objects.create(
            name="test"
        )
        self.activity = Activity.objects.create(
            session_id=self.session,
            exercise_id=self.exercise,
            sets=4,
            repetition=10,
            rest='0:02:00',
            weight=80
        )

    def test_exercise_creation(self):
        exercise = self.exercise
        self.assertTrue(isinstance(exercise, Exercise))
        self.assertEqual(exercise.get_name(), exercise.name)


class MuscleTestCase(TestCase):

    def setUp(self):
        self.exercise = Exercise.objects.create(
            name="test"
        )
        self.muscle = Muscle.objects.create(
            name='muscle'
        )

    def test_muscle_creation(self):
        muscle = self.muscle
        self.assertTrue(isinstance(muscle, Muscle))
        self.assertEqual(muscle.get_user(), muscle.use)
        self.assertEqual(muscle.get_name(), muscle.name)
