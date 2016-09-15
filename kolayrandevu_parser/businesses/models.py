from django.db import models
from django.utils.encoding import force_unicode
from django.utils.safestring import mark_safe

class Business(models.Model):

    created_at = models.DateTimeField(
        auto_now_add=True, editable=False)
    modified_at = models.DateTimeField(
        auto_now=True, editable=False)

    kolayrandevu_url = models.CharField(max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    logo = models.CharField(max_length=1000,null=True, blank=True)
    province = models.CharField(max_length=255,null=True,blank=True)
    district = models.CharField(max_length=255,null=True,blank=True)
    full_address = models.CharField(max_length=255,null=True,blank=True)
    geoposition = models.CharField(max_length=255,null=True,blank=True)
    working_hours = models.CharField(max_length=255,null=True,blank=True)
    about = models.TextField(null=True,blank=True)
    photos = models.TextField(null=True,blank=True)
    professionals = models.TextField(null=True,blank=True)


    class Meta:
        db_table = 'businesses'

    def __unicode__(self):
        return force_unicode(self.name)
    #
    # def image_tag(self):
    #     return mark_safe('<img src="../images/%s" width="150" height="150" />' % (self.logo))
    #
    #
    # image_tag.short_description = 'Image'

    # def __str__(self):
    #     return force_bytes(self.name)
