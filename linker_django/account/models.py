import os
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from django.core.exceptions import ValidationError

class LinkerUser(AbstractUser):
    quote = models.TextField(
        blank=True,
        null=True,
        max_length=300,
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
    )

class Subscription(models.Model):
    follower = models.ForeignKey(
        LinkerUser,
        related_name='following',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        LinkerUser,
        related_name='followers',
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['follower', 'following'], name='unique_subscription')
        ]
    
    def clean(self):
        if self.follower == self.following:
            raise ValidationError("Follower and following cannot be the same.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"
    
def user_photo_path(instance, filename):
    unique_id = instance.linker_user.id
    return f'user_photos/{unique_id}/{filename}'

class LinkerUserPhoto(models.Model):
    linker_user = models.ForeignKey(
        LinkerUser,
        on_delete=models.CASCADE,
        related_name='photos',
    )
    photo = models.ImageField(
        upload_to=user_photo_path,
        default='user_default_photo.png'
    )
    
@receiver(pre_delete, sender=LinkerUserPhoto)
def delete_user_photo(sender, instance, **kwargs):
    instance.photo.delete(True)
