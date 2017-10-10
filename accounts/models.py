from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from jedi.evaluate import instance


class Profile(models.Model):
    user = models.OneToOneField(User)
    profile_img = models.ImageField(null=True)
#     first_name = models.TextField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)
#     city = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(
            user=instance
        )


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()