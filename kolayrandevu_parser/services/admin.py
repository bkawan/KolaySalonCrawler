from django.contrib import admin

# Register your models here.

from .models import Service, BusinessServiceRel,Category

class DateField(admin.ModelAdmin):
    readonly_fields = ['created_at', 'modified_at']

admin.site.register(Service)
admin.site.register(Category)
admin.site.register(BusinessServiceRel, DateField)

