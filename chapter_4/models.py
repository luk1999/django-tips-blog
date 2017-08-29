from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseModel(models.Model):
    @property
    def is_new_record(self):
        return bool(self._state.adding)


class BookCategory(models.Model):
    name = models.CharField(primary_key=True, max_length=30)


class Book(models.Model):
    author = models.ForeignKey('Author')
    category = models.ForeignKey(BookCategory)
    title = models.CharField(max_length=100)


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


class Author(Person):
    pass


class Position(models.Model):
    name = models.CharField(max_length=50)


class Employee(Person):
    position = models.ForeignKey(Position)
