import datetime
from datetime import date
from django.db.models import Sum, F, Q
from spodaily_api import models


class Fitness:

    def get_sessions_by_user(self, user_id):
        sessions = models.Session.objects.filter(user_id=user_id, deleted=False, is_program=False).order_by('-date')
        return sessions

    def get_past_sessions_by_user(self, user_id):
        sessions = models.Session.objects.filter(Q(is_done=True),
                                                 user_id=user_id,
                                                 deleted=False,
                                                 is_program=False) \
            .order_by('-date')
        return sessions

    def get_session_program_by_user(self, user_id):
        sessions = models.Session.objects.filter(user_id=user_id, deleted=False, is_program=True)
        return sessions

    def get_activities_by_session(self, session_id):
        activities = models.Activity.objects.filter(
            session_id=session_id
        ).values(
            'created_at',
            'uuid',
            'sets',
            'repetition',
            'rest',
            'weight',
            'exercise_id',
            'session_id_id',
            'exercise_id__name'
        ).filter(
            deleted=False
        ).order_by('created_at')
        return activities

    def get_session_name_by_act_uuid(self, uuid):
        session = models.Session.objects.filter(uuid=uuid, deleted=False).values('name')
        return session

    def get_muscles(self):
        muscle = list(models.Muscle.objects.filter(deleted=False).values('uuid', 'name'))
        return muscle

    def get_muscle_by_uuid(self, uuid):
        muscle = models.Muscle.objects.filter(uuid=uuid, deleted=False).values('name')
        return muscle

    def get_exercise_by_muscle(self, uuid):
        exercises = list(models.Exercise.objects.filter(muscle__uuid=uuid, deleted=False).values('name'))
        return exercises

    def get_session_number_by_user(self, uuid):
        number = models.Session.objects.filter(deleted=False, user__uuid=uuid, is_done=True, is_program=False).count()
        return number

    def get_tonnage_number_by_user(self, uuid):
        today = date.today()
        number = models.Activity.objects.filter(
            deleted=False,
            session_id__is_done=True,
            session_id__user_id=uuid,
            session_id__is_program=False,
            session_id__deleted=False, session_id__date__lte=today).aggregate(
            sum=Sum(F('weight') * F('repetition') * F('sets')))
        return number

    def get_calories_burn_by_user(self, uuid):
        number = self.get_session_number_by_user(uuid) * 263
        return number

    def get_future_sessions_by_user(self, user_id, number_of_session):
        sessions = models.Session.objects.filter(user_id=user_id, deleted=False, is_program=False,
                                                 is_done=False).order_by('date')[:number_of_session]
        return sessions

    def get_maximum_by_exercise(self, repetition, weight):
        max = int((weight * repetition / 30) + weight)
        return max

    def get_graph_of_exercise(self, request, exercise):
        labels = []
        data = []
        user = request.user
        queryset = models.Activity.objects.filter(session_id__user_id=user,
                                           exercise_id__name=exercise,
                                           deleted=False,
                                           session_id__deleted=False,
                                           session_id__is_done=True,
                                           session_id__is_program=False,
                                           )

        for activity in queryset:
            labels.append(str(activity.session_id.date))
            data.append(self.get_maximum_by_exercise(activity.repetition, activity.weight))

        return labels, data, exercise

    def mark_session_as_done(self, uuid):
        """
        todo CREATE UNIT TEST FOR THIS METHOD
        """
        session_uuid = uuid
        session = models.Session.objects.get(uuid=session_uuid)
        session.is_done = True
        session.save()
        activities = models.Activity.objects.filter(session_id=session_uuid)
        session_2 = session
        session_2.pk = None
        session_2.is_program = False
        session_2.is_done = False
        session_2.date = session.date + datetime.timedelta(days=session.recurrence)
        session_2.save()
        for activity in activities:
            activity_2 = activity
            activity_2.pk = None
            activity_2.session_id = session
            activity_2.save()

    def update_session_settings(self, uuid, form):
        """
        todo CREATE UNIT TEST FOR THIS METHOD
        """
        session_uuid = uuid
        session = models.Session.objects.get(uuid=session_uuid)
        session.recurrence = form.data['recurrence']
        session.name = form.data['name']
        session.save()

    def duplicate_session(self, uuid, form):
        """
        todo CREATE UNIT TEST FOR THIS METHOD
        """
        session_uuid = uuid
        session = models.Session.objects.get(uuid=session_uuid)
        activities = models.Activity.objects.filter(session_id=session_uuid)
        session_2 = session
        session_2.pk = None
        session_2.is_program = False
        session_2.date = form.instance.date
        session_2.save()
        for activity in activities:
            activity_2 = activity
            activity_2.pk = None
            activity_2.session_id = session
            activity_2.save()

    def get_fitness_goals_by_user(self, user_id):
        data = models.FitnessGoal.objects.filter(
            user_id=user_id,
            deleted=False,
            is_done=False
        ).order_by('date')
        return data