from django.contrib import admin
from .models import Project, ProjectEditHistory
# Register your models here.

@admin.register(ProjectEditHistory)
class PublicationEditHistoryAdmin(admin.ModelAdmin):
    list_display = ('project', 'editor', 'edited_at')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title','code', 'is_deleted', 'is_draft', 'is_approved')
    list_filter = ('is_deleted','is_approved','is_draft')
    search_fields = ('title','code')