from django.contrib import admin

# Register your models here.

from .models import Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'Hod')
    search_fields = ('code', 'name', 'Hod__username', 'Hod__email')
