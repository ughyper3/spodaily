from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.datetime_safe import datetime
import uuid as uuid_util


'''

----- COMMON MODELS -----

'''


class CustomManager(models.Manager):
    pass


class MyUserManager(BaseUserManager):

    def create_user(self, email, password):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            password=password
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
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

    sexe_choice = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
        ('Autre', 'Autre')
    ]

    email = models.EmailField(verbose_name='email', max_length=200, unique=True, null=False, blank=False)
    password = models.CharField(max_length=200, null=False, blank=False)
    name = models.CharField(max_length=200, null=True, blank=True, default='')
    first_name = models.CharField(max_length=200, null=True, blank=True, default='')
    birth = models.DateField(null=True, blank=True)
    height = models.SmallIntegerField(null=True, blank=True)
    weight = models.SmallIntegerField(null=True, blank=True)
    number_of_session_per_week = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    average_session_length = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    sexe = models.CharField(null=True, blank=True, choices=sexe_choice, max_length=100)
    picture = models.ImageField(max_length=200, null=True, blank=True)
    accept_email = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'


    def get_email(self):
        return self.email

    def get_password(self):
        return self.password

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Contact(BaseModel):
    CONTACT_CHOICE = [
        ('Suggestion', 'Suggestion'),
        ('Bug', 'Bug'),
        ('Autre', 'Autre')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=CONTACT_CHOICE)
    content = models.CharField(max_length=1000, null=False, blank=False)

    def __str__(self):
        return self.reason

    def get_user(self):
        return self.user


'''

----- FIT MODELS -----

'''


class Session(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    name = models.CharField(max_length=100, null=False, blank=False, default='off')
    recurrence = models.PositiveSmallIntegerField(null=False, blank=False, default=7)
    date = models.DateField(default=datetime.now)
    is_program = models.BooleanField(default=False)
    is_done = models.BooleanField(default=False)

    def get_user(self):
        return self.user

    def get_name(self):
        return self.name


class Exercise(BaseModel):
    name = models.CharField(max_length=200, null=False, blank=False, default="off")

    def __str__(self):
        return self.name

    def get_name(self):
        return self.name


class FitnessGoal(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='exercises')
    weight = models.FloatField(null=False, blank=False, default=0)
    date = models.DateField(default=datetime.now)
    is_done = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name

    def get_weight(self):
        return self.weight

    def get_date(self):
        return self.date


class Activity(BaseModel):
    session_id = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='activity_session_id')
    exercise_id = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.SmallIntegerField(null=False, blank=False, default=0)
    repetition = models.SmallIntegerField(null=False, blank=False, default=0)
    rest = models.DurationField(null=False, blank=False, default='0:00:00')
    weight = models.FloatField(null=False, blank=False, default=0)


    def get_exercise_id(self):
        return self.exercise_id

    def get_sets(self):
        return self.sets

    def get_repetition(self):
        return self.repetition

    def get_rest(self):
        return self.rest

    def get_weight(self):
        return self.weight


class Muscle(BaseModel):
    use = models.ManyToManyField(Exercise)
    name = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.name

    def get_user(self):
        return self.use

    def get_name(self):
        return self.name


'''

----- FIT MODELS -----

'''


class Meal(BaseModel):

    MEAL_CHOICE = (
        ('Petit déjeuner', 'Petit déjeuner'),
        ('Déjeuner', 'Déjeuner'),
        ('Goûté', 'Goûté'),
        ('Diner', 'Diner'),
        ('Collation', 'Collation')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_meal')
    date = models.DateField(default=datetime.now)
    is_done = models.BooleanField(default=False)
    recurrence = models.PositiveSmallIntegerField(blank=False, null=False)
    name = models.CharField(max_length=100, choices=MEAL_CHOICE)

    def __str__(self):
        return self.name


class Food(BaseModel):

    name = models.CharField(max_length=100, null=False, blank=False)
    nutriscore = models.CharField(max_length=2, blank=True, null=True)
    nova = models.PositiveSmallIntegerField(blank=True, null=True)
    eco = models.PositiveSmallIntegerField(blank=True, null=True)
    ean = models.PositiveBigIntegerField(blank=True, null=True)
    kcal = models.PositiveSmallIntegerField(blank=True, null=True)
    proteine = models.PositiveSmallIntegerField(blank=True, null=True)
    glucide = models.PositiveSmallIntegerField(blank=True, null=True)
    lipide = models.PositiveSmallIntegerField(blank=True, null=True)
    sel = models.PositiveSmallIntegerField(blank=True, null=True)
    fibre = models.PositiveSmallIntegerField(blank=True, null=True)
    image = models.CharField(blank=True, null=True, max_length=100)

    def __str__(self):
        return self.name


class MealXFood(BaseModel):

    meal = models.ForeignKey(Meal, on_delete=models.CASCADE, related_name='meal')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='food')
    weight = models.PositiveSmallIntegerField(blank=True, null=True)


