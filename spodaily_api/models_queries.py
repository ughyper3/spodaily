from spodaily_api import models


def get_sessions_by_user(user_id):
    sessions = models.Session.objects.filter(user_id=user_id, deleted=False).order_by('-date')
    return sessions


def get_activities_by_session(session_id):
    activities = models.Activity.objects.filter(
        session_id=session_id
    ).values(
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
    )
    return activities


def get_session_name_by_act_uuid(uuid):
    session = models.Session.objects.filter(uuid=uuid, deleted=False).values('name')
    return session



