from django.contrib import admin
from spodaily_api.models import User, Session, Activity, Exercise, Muscle, Contact, Meal, Food, MealXFood, FitnessGoal


class UserAdmin(admin.ModelAdmin):
    list_display = [
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


class FitnessGoalAdmin(admin.ModelAdmin):
    list_display = [
        "date",
        "user",
        "exercise",
        "weight"
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


class ContactAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "reason",
        "content"
    ]


class MealAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "user",
        "date",
        "is_done"
    ]


class FoodAdmin(admin.ModelAdmin):
    list_display = [
        "name"
    ]


class MealXFoodAdmin(admin.ModelAdmin):
    list_display = [
        "meal",
        "food",
        "weight"
    ]


admin.site.register(User, UserAdmin)
admin.site.register(Session, SessionAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Exercise, ExerciseAdmin)
admin.site.register(FitnessGoal, FitnessGoalAdmin)
admin.site.register(Muscle, MuscleAdmin)
admin.site.register(Contact, ContactAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(MealXFood, MealXFoodAdmin)
