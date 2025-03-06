from django.contrib import admin
from .models import studentDetails
# Register your models here.

@admin.register(studentDetails)
class studentDetailsAdmin(admin.ModelAdmin):
    list_display = ('student', 'faculty_advisor')
    list_filter = ('student', 'faculty_advisor')
    search_fields = ('student', 'faculty_advisor')
    ordering = ('student', 'faculty_advisor')
