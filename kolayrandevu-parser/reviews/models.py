from django.db import models

class ReviewSummary(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(
        auto_now=True, editable=False)

    business = models.OneToOneKey('businesses.Business')
    rating_count = models.PositiveIntegerField
    comment_count = models.PositiveIntegerField