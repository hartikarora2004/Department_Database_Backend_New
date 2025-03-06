from django.urls import path
app_name = 'meeting_report'
from .views import *

urlpatterns = [
    path('bog/',GenerateReport.as_view()),
    path('bog/<int:id>/',GetBog.as_view()),
    path('bog/<int:d_code>/<slug:start_date>/<slug:end_date>/',GenerateBog.as_view()),
    path('dinfo/<int:d_code>/<slug:start_date>/<slug:end_date>/',GenerateDinfo.as_view()),
    path('dinfo/',GenerateDinfo_file.as_view()),
    path('dinfo/<int:id>/',GetDinfo.as_view()),
]