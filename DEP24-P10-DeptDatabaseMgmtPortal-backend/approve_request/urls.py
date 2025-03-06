from django.urls import path
from .views import ApproveRequestCreateView

urlpatterns = [
    path('approval-requests/', ApproveRequestCreateView.as_view(), name='approval-requests-create'),
]
