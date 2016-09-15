from django.contrib import admin

# Register your models here.

from models import Business

class BusinessProfile(admin.ModelAdmin):
    readonly_fields = ['created_at', 'modified_at']




admin.site.register(Business,BusinessProfile)
