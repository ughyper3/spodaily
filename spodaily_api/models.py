from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


class MyUserManager(BaseUserManager):

    def create_user(self, email, user_name, password):

        if not email:
            raise ValueError("Users must have an email address")
        if not user_name:
            raise ValueError("Users must have a username")

        user = self.model(
            email=self.normalize_email(email),
            user_name=user_name,
            password=password,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_name, password):

        user = self.create_user(
            email=self.normalize_email(email),
            user_name=user_name,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser):
    user_name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    email = models.EmailField(verbose_name='email', max_length=200, unique=True, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    name = models.CharField(max_length=200, null=True)
    first_name = models.CharField(max_length=200, null=True)
    birth = models.DateField(null=True)
    height = models.SmallIntegerField(null=True, blank=True)
    weight = models.SmallIntegerField(null=True, blank=True)
    picture = models.ImageField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
