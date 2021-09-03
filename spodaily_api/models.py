from django.db import models
from django.utils import timezone


class User(models.Model):

    admin = 'admin'
    free = 'free'
    premium = 'premium'

    status_choices = [
        (admin, 'admin'),
        (free, 'free'),
        (premium, 'premium'),
    ]

    user_name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    email = models.EmailField(max_length=200, unique=True, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    birth = models.DateField(null=True)
    height = models.SmallIntegerField(null=True, blank=True)
    weight = models.SmallIntegerField(null=True, blank=True)
    picture = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(choices=status_choices, max_length=200)
    created_at = models.DateTimeField(default=timezone.now)


