from django.contrib import admin
from .models import ApproveRequest

@admin.register(ApproveRequest)
class ApproveRequestAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'request_date')
