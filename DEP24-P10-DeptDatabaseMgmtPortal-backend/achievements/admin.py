from django.contrib import admin
from .models import Achievement , AchievementEditHistory

@admin.register(AchievementEditHistory)
class AchievementEditHistoryAdmin(admin.ModelAdmin):
    list_display = ('achievement', 'editor', 'edited_at')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_deleted', 'is_draft', 'is_approved')
    list_filter = ('is_deleted','is_approved','is_draft')
    search_fields = ('title',)