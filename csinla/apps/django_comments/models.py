from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_comments.signals import comment_was_posted

from .abstracts import (
    COMMENT_MAX_LENGTH, BaseCommentAbstractModel, CommentAbstractModel,
)


class Comment(CommentAbstractModel):
    class Meta(CommentAbstractModel.Meta):
        db_table = "django_comments"


@python_2_unicode_compatible
class CommentFlag(models.Model):
    """
    Records a flag on a comment. This is intentionally flexible; right now, a
    flag could be:

        * A "removal suggestion" -- where a user suggests a comment for (potential) removal.

        * A "moderator deletion" -- used when a moderator deletes a comment.

    You can (ab)use this model to add other flags, if needed. However, by
    design users are only allowed to flag a comment with a given flag once;
    if you want rating look elsewhere.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, verbose_name=_('user'), related_name="comment_flags",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        # Translators: 'comment' is a noun here.
        Comment, verbose_name=_('comment'), related_name="flags", on_delete=models.CASCADE,
    )
    # Translators: 'flag' is a noun here.
    flag = models.CharField(_('flag'), max_length=30, db_index=True)
    flag_date = models.DateTimeField(_('date'), default=None)

    # Constants for flag types
    SUGGEST_REMOVAL = "removal suggestion"
    MODERATOR_DELETION = "moderator deletion"
    MODERATOR_APPROVAL = "moderator approval"

    class Meta:
        db_table = 'django_comment_flags'
        unique_together = [('user', 'comment', 'flag')]
        verbose_name = _('comment flag')
        verbose_name_plural = _('comment flags')

    def __str__(self):
        return "%s flag of comment ID %s by %s" % (
            self.flag, self.comment_id, self.user.get_username()
        )

    def save(self, *args, **kwargs):
        if self.flag_date is None:
            self.flag_date = timezone.now()
        super(CommentFlag, self).save(*args, **kwargs)

class UserNotificationsCount(models.Model):
    user_id = models.IntegerField()
    has_readed = models.BooleanField(default=False)
    #unread_count = models.IntegerField(default=0)
    comment = models.ForeignKey(Comment, on_delete = models.CASCADE, null = True, blank = True)
    def __str__(self):
        return '<UserNotificationsCount %s: %s>' % (self.user_id, self.has_readed)


def post_post_save(sender, comment, request, *args, **kwargs):
    post = comment
    if post.superior:
        from csinla_accounts.models import Profile
        su_id = Profile.objects.get(email=post.superior)
        event = UserNotificationsCount(user_id=su_id.id, comment = post)
        event.save()
    event = UserNotificationsCount(user_id=post.content_object.author.id, comment = post)
    event.save()

comment_was_posted.connect(post_post_save)
