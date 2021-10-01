from django.contrib import admin
from spodaily_api.models import User, Routine, Session, Activity, Exercise, Muscle


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "user_name",
        "email",
    ]


class RoutineAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


class SessionAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "name"
    ]


class ActivityAdmin(admin.ModelAdmin):
    list_display = [
        "session_id",
        "exercise_id",
        "sets",
        "repetition",
        "rest",
        "weight"
    ]


class ExerciseAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


class MuscleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Routine, RoutineAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(Muscle, MuscleAdmin)
