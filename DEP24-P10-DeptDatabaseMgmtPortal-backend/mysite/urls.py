from django.contrib import admin
from django.urls import path, include
from user_queries.views import createView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usercustom.urls')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('department/', include('department.urls')),
    path('batch/', include('batch.urls')),
    path('notifications/', include('notifications.urls')),
    path('research_labs/', include('research_lab.urls')),
    path('publications/', include('publications.urls')),
    path('projects/', include('project.urls')),
    path('student/projects/', include('student_project.urls')),
    path('achievements/', include('achievements.urls')),
    path('events/', include('events.urls')),
    path('visits/', include('visits.urls')),
    path('reports/', include('meeting_reports.urls')),
    path('query/', createView.as_view(), name='query'),
    path('api/faculty/', include('faculty_details.urls')),  # include app-level urls'
    path('api/', include('approve_request.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)