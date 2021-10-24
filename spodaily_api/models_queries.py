from spodaily_api import models
from spodaily_api.models import Muscle, Exercise


def get_sessions_by_user(user_id):
    sessions = models.Session.objects.filter(user_id=user_id, deleted=False).order_by('-date')
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