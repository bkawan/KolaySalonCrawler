from django.db import models
from businesses.models import Business
from django.utils.encoding import force_unicode


class ReviewSummary(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(
        auto_now=True, editable=False)

    business = models.ForeignKey(Business)
    rating_count = models.PositiveIntegerField(null=True, blank=True)
    comment_count = models.PositiveIntegerField(null=True, blank=True)

    class Meta:
        db_table = 'reviews'

    def __unicode__(self):
        return force_unicode(
            "{0} - {1}".format(self.business, self.rating_count)
        )
