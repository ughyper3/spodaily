from django.test import TestCase
from spodaily_api.models import Exercise, Muscle
from spodaily_api.views import *


class HomeTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_home_not_authenticated_user(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/home.html')
        self.assertEqual(response.status_code, 302)

    def test_home_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/home.html')
        self.client.logout()


class AddFutureSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_add_session_not_authenticated_user(self):
        url = reverse('add_session')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/add_session.html')
        self.assertEqual(response.status_code, 302)

    def test_add_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('add_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/add_session.html')
        self.client.logout()


class PastSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_past_session_not_authenticated_user(self):
        url = reverse('past_session')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/session.html')
        self.assertEqual(response.status_code, 302)

    def test_past_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('past_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/session.html')
        self.client.logout()


class ExerciseGuideTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_exercise_guide_not_authenticated_user(self):
        url = reverse('exercise_guide')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/exercise_guide.html')
        self.assertEqual(response.status_code, 302)

    def test_exercise_guide_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('exercise_guide'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/exercise_guide.html')
        self.client.logout()


class AddFutureActivityTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_add_activity_not_authenticated_user(self):
        url = reverse('add_future_activity', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/add_activity.html')
        self.assertEqual(response.status_code, 302)

    def test_add_activity_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('add_future_activity', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/add_activity.html')
        self.client.logout()


class DeletePastSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_past_delete_session_not_authenticated_user(self):
        url = reverse('delete_past_session', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/delete_session.html')
        self.assertEqual(response.status_code, 302)

    def test_past_delete_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('delete_past_session', args=[self.session.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/delete_session.html')
        self.client.logout()


class DeleteActivityTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')
        self.exercise = Exercise.objects.create(name='test')
        self.activity = Activity.objects.create(session_id=self.session, exercise_id=self.exercise, rest='0:02:00')

    def test_delete_activity_not_authenticated_user(self):
        url = reverse('delete_activity', args=[self.activity.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/delete_activity.html')
        self.assertEqual(response.status_code, 302)

    def test_delete_activity_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('delete_activity', args=[self.activity.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/delete_activity.html')
        self.client.logout()


class RoutineTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_routine_not_authenticated_user(self):
        url = reverse('routine')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/routine.html')
        self.assertEqual(response.status_code, 302)

    def test_routine_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('routine'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/routine.html')
        self.client.logout()


class PastSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_past_session_not_authenticated_user(self):
        url = reverse('past_session')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/past_session.html')
        self.assertEqual(response.status_code, 302)

    def test_past_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('past_session'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/past_session.html')
        self.client.logout()


class MuscleTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.exercise = Exercise.objects.create(name='test')
        self.exercises = Exercise.objects.filter()
        self.muscle = Muscle.objects.create(name='test')
        self.muscle.use.set(self.exercises)

    def test_muscle_of_use_not_authenticated_user(self):
        url = reverse('muscle', args=[self.muscle.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/muscle.html')
        self.assertEqual(response.status_code, 302)

    def test_muscle_of_use_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('muscle', args=[self.muscle.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/muscle.html')
        self.client.logout()