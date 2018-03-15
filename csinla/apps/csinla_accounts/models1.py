from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from csinla_posts.models import Post
# from django.utils import timezone
from django.db.models.signals import post_save


class Profile(models.Model):

    REG_TYPE = (
        ('STU', 'student'),
        ('COM', 'company'),
    )

    GENDER = (
        ('F', 'female'),
        ('M', 'male'),
        ('U', 'unknown'),
    )

    user = models.OneToOneField(
        User,
        related_name = 'profile',
        on_delete = models.CASCADE,
    )

    reg_type = models.CharField(
        max_length = 10,
        choices = REG_TYPE,
        default = 'STU',
    )

    real_name = models.CharField(
        max_length = 50,
        blank = True,
    )

    gender = models.CharField(
        max_length = 1,
        choices = GENDER,
        default = 'F',
    )

    birth_date = models.DateField(
        null = True,
        blank = True,
    )

    school = models.CharField(
        max_length = 200,
        default = '',
    )

    phone = models.CharField(
        max_length = 11,
        default = '',
    )

    avatar = models.ImageField(
        upload_to = 'avatars/',
        default = 'avatars/moon.jpg',
    )

    personal_level = models.IntegerField(
        default = 0,
    )

    academic_rank = models.IntegerField(
        default = 0,
    )

    self_intro = models.CharField(
        max_length = 200,
        blank = True,
    )

    favourite_posts = models.ManyToManyField(
        Post,
        related_name = 'favourite_posts'
    )

    follows = models.ManyToManyField(
        User,
        related_name='follows',
        symmetrical = False,
    )


    # reg_time = models.DateTimeField(
    #     #auto_now_add = True,
    #     default = timezone.now,
    # )

    duoshuo_id = models.IntegerField(
            default = 0
    )

    def __unicode__(self):
        return self.user.username

# signal
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)

