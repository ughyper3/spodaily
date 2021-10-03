from spodaily_api import models


def get_routine_by_user(user_id):
    data = models.Routine.objects.filter(user_id=user_id)
    return data


def get_sessions_by_routine(routine_id):
    sessions = models.Session.objects.filter(routine_id_id=routine_id)
    return sessions


def get_activities_by_session(session_id):
    activities = models.Activity.objects.filter(
        session_id=session_id
    ).values(
        'sets',
        'repetition',
        'rest',
        'weight',
        'exercise_id_id',
        'session_id_id',
        'exercise_id__name'
    )
    return activities


def get_session_name_by_act_uuid(uuid):
    session = models.Session.objects.filter(uuid=uuid).values('name')
    return session



