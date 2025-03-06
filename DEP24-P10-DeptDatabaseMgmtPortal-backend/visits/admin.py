from django.contrib import admin

# Register your models here.

from .models import Visit

@admin.register(Visit)
class VisitAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'is_deleted', 'is_draft', 'is_approved')
    list_filter = ('is_deleted','is_approved','is_draft')
    search_fields = ('title',)