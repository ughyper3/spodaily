from django.test import TestCase
from spodaily_api.models import Exercise, Muscle
from spodaily_api.views import *


class HomeTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(date=datetime.date.today(), user=self.pascal)
        self.session2 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_done=True)
        self.sdt = Exercise.objects.create(name='Soulevé de terre')
        self.squat = Exercise.objects.create(name='Squat')
        self.dc = Exercise.objects.create(name='Développé couché')
        self.activity = Activity.objects.create(session_id=self.session, exercise_id=self.sdt)
        self.activity1 = Activity.objects.create(session_id=self.session2, exercise_id=self.sdt)
        self.activity2 = Activity.objects.create(session_id=self.session2, exercise_id=self.squat)
        self.activity3 = Activity.objects.create(session_id=self.session2, exercise_id=self.dc)

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

        self.assertEqual(len(response.context['session']), 1)
        self.assertEqual(type(response.context['session'][0]), dict)

        self.assertEqual(len(response.context['activity']), 1)
        self.assertEqual(type(response.context['activity']), list)
        self.assertEqual(len(response.context['activity'][0]), 1)
        self.assertEqual(type(response.context['activity'][0][0]), dict)

        self.assertEqual(len(response.context['sdt_labels']), 1)
        self.assertEqual(type(response.context['sdt_labels']), list)
        self.assertEqual(type(response.context['sdt_labels'][0]), str)

        self.assertEqual(len(response.context['squat_labels']), 1)
        self.assertEqual(type(response.context['squat_labels']), list)
        self.assertEqual(type(response.context['squat_labels'][0]), str)

        self.assertEqual(len(response.context['bench_labels']), 1)
        self.assertEqual(type(response.context['bench_labels']), list)
        self.assertEqual(type(response.context['bench_labels'][0]), str)

        self.assertEqual(len(response.context['sdt_data']), 1)
        self.assertEqual(type(response.context['sdt_data']), list)
        self.assertEqual(type(response.context['sdt_data'][0]), int)

        self.assertEqual(len(response.context['squat_data']), 1)
        self.assertEqual(type(response.context['squat_data']), list)
        self.assertEqual(type(response.context['squat_data'][0]), int)

        self.assertEqual(len(response.context['bench_data']), 1)
        self.assertEqual(type(response.context['bench_data']), list)
        self.assertEqual(type(response.context['bench_data'][0]), int)

        self.assertEqual(type(response.context['number_of_session']), int)

        self.assertEqual(type(response.context['number_of_tonnage']), float)

        self.assertEqual(type(response.context['number_of_session']), int)

        self.assertEqual(type(response.context['number_of_calories']), int)

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
        self.session2 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_done=True)
        self.sdt = Exercise.objects.create(name='Soulevé de terre')
        self.squat = Exercise.objects.create(name='Squat')
        self.dc = Exercise.objects.create(name='Développé couché')
        self.activity1 = Activity.objects.create(session_id=self.session2, exercise_id=self.sdt)
        self.activity2 = Activity.objects.create(session_id=self.session2, exercise_id=self.squat)
        self.activity3 = Activity.objects.create(session_id=self.session2, exercise_id=self.dc)

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

        self.assertEqual(len(response.context['session']), 1)
        self.assertEqual(type(response.context['session'][0]), dict)

        self.assertEqual(len(response.context['activity']), 1)
        self.assertEqual(len(response.context['activity'][0]), 3)
        self.assertEqual(type(response.context['activity']), list)
        self.assertEqual(type(response.context['activity'][0][0]), dict)
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


class AddProgramActivityTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_add_activity_not_authenticated_user(self):
        url = reverse('add_program_activity', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/add_activity.html')
        self.assertEqual(response.status_code, 302)

    def test_add_activity_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('add_program_activity', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/add_activity.html')
        self.client.logout()


class DeleteFutureSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_past_delete_session_not_authenticated_user(self):
        url = reverse('delete_future_session', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/delete_session.html')
        self.assertEqual(response.status_code, 302)

    def test_past_delete_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('delete_future_session', args=[self.session.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/delete_session.html')
        self.client.logout()


class DeleteProgramSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_past_delete_session_not_authenticated_user(self):
        url = reverse('delete_program_session', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/delete_session.html')
        self.assertEqual(response.status_code, 302)

    def test_past_delete_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('delete_program_session', args=[self.session.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/delete_session.html')
        self.client.logout()


class DeleteFutureActivityTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')
        self.exercise = Exercise.objects.create(name='test')
        self.activity = Activity.objects.create(session_id=self.session, exercise_id=self.exercise, rest='0:02:00')

    def test_delete_activity_not_authenticated_user(self):
        url = reverse('delete_future_activity', args=[self.activity.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/delete_activity.html')
        self.assertEqual(response.status_code, 302)

    def test_delete_activity_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('delete_future_activity', args=[self.activity.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/delete_activity.html')
        self.client.logout()


class DeleteProgramActivityTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')
        self.exercise = Exercise.objects.create(name='test')
        self.activity = Activity.objects.create(session_id=self.session, exercise_id=self.exercise, rest='0:02:00')

    def test_delete_activity_not_authenticated_user(self):
        url = reverse('delete_program_activity', args=[self.activity.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/delete_activity.html')
        self.assertEqual(response.status_code, 302)

    def test_delete_activity_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('delete_program_activity', args=[self.activity.uuid]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/delete_activity.html')
        self.client.logout()


class RoutineTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(date=datetime.date.today(), user=self.pascal)
        self.sdt = Exercise.objects.create(name='Soulevé de terre')
        self.squat = Exercise.objects.create(name='Squat')
        self.dc = Exercise.objects.create(name='Développé couché')
        self.activity = Activity.objects.create(session_id=self.session, exercise_id=self.sdt)


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

        self.assertEqual(len(response.context['session']), 1)
        self.assertEqual(type(response.context['session'][0]), dict)

        self.assertEqual(len(response.context['activity']), 1)
        self.assertEqual(type(response.context['activity']), list)
        self.assertEqual(type(response.context['activity'][0][0]), dict)

        self.client.logout()


class FutureSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_future_session_not_authenticated_user(self):
        url = reverse('routine')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/routine.html')
        self.assertEqual(response.status_code, 302)

    def test_past_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('routine'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/routine.html')
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


class UpdateProgramSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.exercise = Exercise.objects.create(name='test')
        self.session = Session.objects.create(user=self.pascal, name='test_session')
        self.activity = Activity.objects.create(session_id=self.session, exercise_id=self.exercise)

    def test_update_not_authenticated_user(self):
        url = reverse('update_program_activity', args=[self.activity.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/update_activity.html')

    def test_update_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('update_program_activity', args=[self.activity.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/update_activity.html')
        self.client.logout()


class UpdateFutureSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.exercise = Exercise.objects.create(name='test')
        self.session = Session.objects.create(user=self.pascal, name='test_session')
        self.activity = Activity.objects.create(session_id=self.session, exercise_id=self.exercise)

    def test_update_not_authenticated_user(self):
        url = reverse('update_future_activity', args=[self.activity.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/update_activity.html')

    def test_update_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('update_future_activity', args=[self.activity.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/update_activity.html')
        self.client.logout()


class ProgramTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_program_not_authenticated_user(self):
        url = reverse('program')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/program.html')
        self.assertEqual(response.status_code, 302)

    def test_program_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        response = self.client.get(reverse('program'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/program.html')
        self.client.logout()


class AddProgramSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')

    def test_add_activity_not_authenticated_user(self):
        url = reverse('add_program_session')
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/add_program_session.html')
        self.assertEqual(response.status_code, 302)

    def test_add_activity_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('add_program_session')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/add_program_session.html')
        self.client.logout()


class DuplicateSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_duplicate_session_not_authenticated_user(self):
        url = reverse('duplicate_program_session', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/duplicate_program_session.html')
        self.assertEqual(response.status_code, 302)

    def test_duplicate_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('duplicate_program_session', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/duplicate_program_session.html')
        self.client.logout()


class MarkSessionAsDoneTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_mark_as_done_session_not_authenticated_user(self):
        url = reverse('session_done', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/session_done.html')
        self.assertEqual(response.status_code, 302)

    def test_duplicate_session_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('session_done', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/session_done.html')
        self.client.logout()


class SettingsProgramSessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(user=self.pascal, name='test_session')

    def test_SettingsProgramSession_not_authenticated_user(self):
        url = reverse('settings_program_session', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertTemplateNotUsed(response, 'spodaily_api/fit/settings_programme_session.html')
        self.assertEqual(response.status_code, 302)

    def test_SettingsProgramSession_authenticated_user(self):
        self.client.login(email='pascal@test.com', password='pascal')
        url = reverse('settings_program_session', args=[self.session.uuid])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'spodaily_api/fit/settings_programme_session.html')
        self.client.logout()
