from django.contrib import admin

# Register your models here.

from .models import ResearchLab

@admin.register(ResearchLab)
class ResearchLabAdmin(admin.ModelAdmin):
    list_display = ('code', 'Head', 'is_deleted', 'is_draft', 'is_approved')
    list_filter = ('is_deleted','is_approved','is_draft')
    search_fields = ('code', 'name', 'Head__username', 'Head__email')