from django.contrib import admin
from spodaily_api.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = [
        "status",
        "user_name",
        "email",
    ]


admin.site.register(User, UserAdmin)
