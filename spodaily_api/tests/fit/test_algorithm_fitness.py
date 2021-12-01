import datetime
from django.test import TestCase
from spodaily_api.algorithm.fitness import Fitness
from spodaily_api.models import User, Session, Activity, Exercise, Muscle


class GetSessionByUserTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.pascal2 = User.objects.create_user(email='pascal2@test.com', password='pascal2')
        self.session1 = Session.objects.create(date=datetime.date.today(), user=self.pascal)
        self.session2 = Session.objects.create(date=datetime.date.today(), user=self.pascal2)
        self.session3 = Session.objects.create(date=datetime.date.today(), user=self.pascal, deleted=True)
        self.session4 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_program=True)
        self.session5 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_done=True)
        self.session6 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_done=False)

    def test_get_sessions_by_user(self):
        fitness = Fitness()
        self.assertEqual(fitness.get_sessions_by_user(self.pascal.uuid).count(), 3)
        self.assertEqual(fitness.get_session_number_by_user(self.pascal.uuid), 1)
        self.assertEqual(fitness.get_calories_burn_by_user(self.pascal.uuid), 263)
        self.assertEqual(fitness.get_future_sessions_by_user(self.pascal.uuid, 5).count(), 2)


class GetPastSessionByUserTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.pascal2 = User.objects.create_user(email='pascal2@test.com', password='pascal2')
        self.session1 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_done=True)
        self.session2 = Session.objects.create(date=datetime.date.today(), user=self.pascal2, is_done=True)
        self.session3 = Session.objects.create(date=datetime.date.today(), user=self.pascal, deleted=True)
        self.session4 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_program=True)

    def test_get_past_sessions_by_user(self):
        fitness = Fitness()
        self.assertEqual(fitness.get_past_sessions_by_user(self.pascal.uuid).count(), 1)


class GetSessionProgramByUserTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.pascal2 = User.objects.create_user(email='pascal2@test.com', password='pascal2')
        self.session1 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_done=True)
        self.session2 = Session.objects.create(date=datetime.date.today(), user=self.pascal2, is_done=True)
        self.session3 = Session.objects.create(date=datetime.date.today(), user=self.pascal, deleted=True)
        self.session4 = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_program=True)

    def test_get_session_program_by_user(self):
        fitness = Fitness()
        self.assertEqual(fitness.get_session_program_by_user(self.pascal.uuid).count(), 1)


class GetActivitiesBySessionTest(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_done=True)
        self.exercise = Exercise.objects.create(name='test')
        self.activity1 = Activity.objects.create(session_id=self.session, exercise_id=self.exercise, weight=100, sets=2, repetition=10)
        self.activity2 = Activity.objects.create(session_id=self.session, exercise_id=self.exercise, deleted=True)

    def test_get_session_program_by_user(self):
        fitness = Fitness()
        self.assertEqual(fitness.get_activities_by_session(self.session.uuid).count(), 1)
        self.assertEqual(fitness.get_tonnage_number_by_user(self.pascal.uuid)['sum'], 2000.0)
        self.assertEqual(fitness.get_maximum_by_exercise(self.activity1.repetition, self.activity1.weight), 133)


class GetSessionsNameByActUuid(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.session = Session.objects.create(date=datetime.date.today(), user=self.pascal, is_done=True, name='testz')
        self.exercise = Exercise.objects.create(name='test')
        self.activity1 = Activity.objects.create(session_id=self.session, exercise_id=self.exercise)
        self.activity2 = Activity.objects.create(session_id=self.session, exercise_id=self.exercise, deleted=True)

    def test_get_session_name_by_act_uuid(self):
        fitness = Fitness()
        self.assertEqual(fitness.get_session_name_by_act_uuid(self.session.uuid)[0]['name'], 'testz')


class GetMuscles(TestCase):

    def setUp(self):
        self.exercise = Exercise.objects.create(name='test')
        self.muscle = Muscle.objects.create(name='m1')
        self.muscle2 = Muscle.objects.create(name='m2')
        self.muscle3 = Muscle.objects.create(name='m3')
        self.muscle4 = Muscle.objects.create(name='m4', deleted=True)

    def test_get_muscles(self):
        fitness = Fitness()
        self.assertEqual(len(fitness.get_muscles()), 3)
        self.assertEqual(fitness.get_muscle_by_uuid(self.muscle2.uuid)[0]['name'], 'm2')


class GetExercise(TestCase):

    def setUp(self):
        self.exercise = Exercise.objects.create(name='test')
        self.exercise2 = Exercise.objects.create(name='test2')
        self.exercise3 = Exercise.objects.create(name='test3', deleted=True)
        self.muscle = Muscle.objects.create(name='m1')
        self.muscle.use.add(self.exercise, self.exercise2, self.exercise3)

    def test_get_exercises(self):
        fitness = Fitness()
        self.assertEqual(len(fitness.get_exercise_by_muscle(self.muscle.uuid)), 2)


class GetFitnessGoalsByUser(TestCase):

    def setUp(self):
        self.pascal = User.objects.create_user(email='pascal@test.com', password='pascal')
        self.exercise = Exercise.objects.create(name='test')
        self.goal = Fitness(goal)


