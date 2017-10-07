from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)
#     first_name = models.TextField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     city = models.CharField(max_length=30, blank=True)


