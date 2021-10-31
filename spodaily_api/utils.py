from datetime import date

from django.shortcuts import render

from spodaily_api.models import Activity


def get_maximum_by_exercise(repetition, weight):
    max = int((weight * repetition / 30) + weight)
    return max


def get_graph_of_exercise(request, exercise):
    labels = []
    data = []
    user = request.user
    today = date.today()
    queryset = Activity.objects.filter(session_id__user_id=user, exercise_id__name=exercise, deleted=False, session_id__date__lt=today)

    for activity in queryset:
        labels.append(str(activity.session_id.date))
        data.append(get_maximum_by_exercise(activity.repetition, activity.weight))

    return labels, data, exercise