from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# файл models.py это орм. Каждый класс это таблица в базе данных,
# поля класса это столбцы в базе


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.CharField(max_length=100)

    # этот метод - конструктор
    # в данном случае будет отражать имя топика в админке
    def __str__(self):
        return self.name


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    last_updated = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, related_name='topics')
    starter = models.ForeignKey(User, related_name='topics')

    def __str__(self):
        return self.subject


class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    created_by = models.ForeignKey(User, related_name='posts')
    updated_by = models.ForeignKey(User, null=True, related_name='+')

    def __str__(self):
        return self.topic.subject


class Comments(models.Model):
    creator = models.ForeignKey(User, related_name='comment')
    body = models.TextField(max_length=4000)
    post = models.ForeignKey(Post, related_name='comment', null=True)
    created_at = models.DateTimeField(default=now)

    def __str__(self):
        return self.body
