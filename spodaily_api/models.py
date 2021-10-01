from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.datetime_safe import datetime
import uuid as uuid_util


class CustomManager(models.Manager):
    pass


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

    def create_superuser(self, email, user_name, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            user_name=user_name,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid_util.uuid4)
    created_at = models.DateTimeField(default=datetime.now)
    deleted = models.BooleanField(default=False)

    objects = CustomManager()

    class Meta:
        abstract = True

    abstract = True

    def delete(self, **kwargs):
        self.deleted = True
        self.save()


class User(AbstractBaseUser, BaseModel):
    user_name = models.CharField(max_length=200, unique=True, null=False, blank=False)
    email = models.EmailField(verbose_name='email', max_length=200, unique=True, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    name = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    birth = models.DateField(null=True, blank=True)
    height = models.SmallIntegerField(null=True, blank=True)
    weight = models.SmallIntegerField(null=True, blank=True)
    picture = models.ImageField(max_length=200, null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_name']

    def __str__(self):
        return self.user_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Routine(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    date_start = models.DateField(default=datetime.now)
    session_per_week = models.SmallIntegerField(null=False, blank=False, default=3)


class Session(BaseModel):
    routine_id = models.ForeignKey(Routine, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False, blank=False, default='off')
    date = models.DateField(default=datetime.now)


class Activity(BaseModel):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='activity_session_id')
    exercise_id = models.ForeignKey(Session, on_delete=models.CASCADE)
    sets = models.SmallIntegerField(null=False, blank=False, default=0)
    repetition = models.SmallIntegerField(null=False, blank=False, default=0)
    rest = models.DurationField(null=False, blank=False, default=0)
    weight = models.SmallIntegerField(null=False, blank=False, default=0)


class Exercise(BaseModel):
    name = models.CharField(max_length=200, null=False, blank=False, default="off")



class Muscle(BaseModel):
    use = models.ManyToManyField(Exercise)
    name = models.CharField(max_length=100, null=False, blank=False)
