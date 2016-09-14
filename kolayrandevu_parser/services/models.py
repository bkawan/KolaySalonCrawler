from django.db import models

from businesses.models import Business
from django.utils.encoding import force_unicode


class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'categories'

    def __unicode__(self):
        return force_unicode(self.name)


class Service(models.Model):
    category = models.ForeignKey(Category)
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'services'

    def __unicode__(self):
        return force_unicode(self.name)


class BusinessServiceRel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(auto_now=True, editable=False)
    GENDERS = (
        ('m', 'Men'),
        ('w', 'Women'),
    )

    business = models.ForeignKey(Business)
    service = models.ForeignKey(Service)
    gender = models.CharField(max_length=1, choices=GENDERS)
    price = models.CharField(max_length=50)

    class Meta:
        db_table = 'business_services_rels'

    def __unicode__(self):
        return force_unicode(self.service)
