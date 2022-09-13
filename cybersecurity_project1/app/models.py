from distutils.command.upload import upload
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    following = models.ManyToManyField(
        "self",
        related_name="follower",
        symmetrical=False
    )

    bio = models.TextField(
        max_length=500,
        blank=True
    )

    @property
    def followers(self):
        return Profile.objects.get

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **_):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **_):
    instance.profile.save()

class Post(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    public = models.BooleanField()
    upload_date = models.DateTimeField()
    content = models.TextField(
        max_length=500,
        blank=True
    )

    @property
    def attachments(self):
        return PostAttachment.objects.filter(post_id=self.id)


def post_attachment_upload_to (i, fname):
    return 'attachments/post_attachment_%d/%s_%s' % (i.post.profile.id, i.post.profile.user.username, fname)

class PostAttachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content_type = models.TextField(
        max_length=500,
        blank=False
    )
    content = models.FileField(
        upload_to=post_attachment_upload_to
    )
