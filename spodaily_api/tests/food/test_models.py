from django.test import TestCase
from spodaily_api.models import Meal, User, Food, MealXFood


class MealTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.test",
            password="testtesttest"
        )
        self.meal = Meal.objects.create(
            user=self.user,
            recurrence=7,
            name='Petit déjeuner'
        )

    def test_session_creation(self):
        meal = self.meal
        self.assertTrue(isinstance(meal, Meal))


class FoodTestCase(TestCase):

    def setUp(self):
        self.food = Food.objects.create(
            name='test',
        )

    def test_session_creation(self):
        food = self.food
        self.assertTrue(isinstance(food, Food))


class MealXFoodTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            email="test@test.test",
            password="testtesttest"
        )
        self.meal = Meal.objects.create(
            user=self.user,
            recurrence=7,
            name='Petit déjeuner'
        )
        self.food = Food.objects.create(
            name='test'
        )
        self.mealxfood = MealXFood.objects.create(
            meal=self.meal,
            food=self.food,
            weight=100
        )

    def test_session_creation(self):
        food = self.food
        self.assertTrue(isinstance(food, Food))