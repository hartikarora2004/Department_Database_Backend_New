from django.contrib import admin
from .models import StudentProject
# Register your models here.

@admin.register(StudentProject)
class StudentProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted', 'is_draft', 'is_approved')
    list_filter = ('is_deleted','is_approved','is_draft')
    search_fields = ('title',)