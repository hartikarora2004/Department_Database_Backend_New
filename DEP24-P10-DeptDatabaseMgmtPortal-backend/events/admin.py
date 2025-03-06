from django.contrib import admin

# Register your models here.

from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted', 'is_draft', 'is_approved')
    list_filter = ('is_deleted','is_approved','is_draft')
    search_fields = ('title',)