from django.contrib import admin

# Register your models here.
from .models import QueryModel

# admin.site.register(QueryModel)
@admin.register(QueryModel)
class QueryAdmin(admin.ModelAdmin):
    list_display = ('issue_category', 'issue', 'issue_status', 'issue_assigned')
    list_filter = ('issue_category', 'issue_status', 'issue_assigned')
    search_fields = ('issue_category', 'issue_status', 'issue_assigned', 'issue')