from django.contrib import admin

from models import ReviewSummary
# Register your models here.

class DateField(admin.ModelAdmin):
    readonly_fields = ['created_at', 'modified_at']

admin.site.register(ReviewSummary,DateField)
