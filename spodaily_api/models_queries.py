from datetime import date

from django.db.models import Sum, F, Q

from spodaily_api import models
from spodaily_api.models import Muscle, Exercise, Session, Activity


def get_sessions_by_user(user_id):
    sessions = models.Session.objects.filter(user_id=user_id, deleted=False, is_program=False).order_by('-date')
    return sessions


def get_past_sessions_by_user(user_id):
    sessions = models.Session.objects.filter(Q(is_done=True),
                                             user_id=user_id,
                                             deleted=False,
                                             is_program=False)\
        .order_by('-date')
    return sessions


def get_session_program_by_user(user_id):
    sessions = models.Session.objects.filter(user_id=user_id, deleted=False, is_program=True)
    return sessions


def get_activities_by_session(session_id):
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


def get_session_name_by_act_uuid(uuid):
    session = models.Session.objects.filter(uuid=uuid, deleted=False).values('name')
    return session


def get_muscles():
    muscle = list(Muscle.objects.filter(deleted=False).values('uuid', 'name'))
    return muscle


def get_muscle_by_uuid(uuid):
    muscle = models.Muscle.objects.filter(uuid=uuid, deleted=False).values('name')
    return muscle


def get_exercise_by_muscle(uuid):
    exercises = list(Exercise.objects.filter(muscle__uuid=uuid, deleted=False).values('name'))
    return exercises


def get_session_number_by_user(uuid):
    number = Session.objects.filter(deleted=False, user__uuid=uuid, is_done=True, is_program=False).count()
    return number


def get_tonnage_number_by_user(uuid):
    today = date.today()
    number = Activity.objects.filter(
        deleted=False,
        session_id__is_done=True,
        session_id__user_id=uuid,
        session_id__is_program=False,
        session_id__deleted=False, session_id__date__lte=today).aggregate(sum=Sum(F('weight') * F('repetition') * F('sets')))
    return number


def get_calories_burn_by_user(uuid):
    number = get_session_number_by_user(uuid) * 263
    return number


def get_future_sessions_by_user(user_id, number_of_session):
    sessions = models.Session.objects.filter(user_id=user_id, deleted=False, is_program=False, is_done=False).order_by('date')[:number_of_session]
    return sessions

