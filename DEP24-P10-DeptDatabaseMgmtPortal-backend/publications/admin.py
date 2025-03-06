from django.contrib import admin
from .models import Publication, PublicationEditHistory

@admin.register(PublicationEditHistory)
class PublicationEditHistoryAdmin(admin.ModelAdmin):
    list_display = ('publication', 'editor', 'edited_at')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'identifier', 'identifier_type', 'is_deleted', 'is_draft', 'is_approved')
    list_filter = ('is_deleted', 'is_approved', 'is_draft')
    search_fields = ('title', 'identifier')