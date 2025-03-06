from django.urls import path
from .views import *

urlpatterns = [
  path("get-details",UserView.as_view()),
  path('user/list',userListAPI.as_view()),
  path('login',login_page),
  path('verify',otp_verify),
  path('user/definitions/',definations),
  path('user/<int:id>/', UserDetailAPI.as_view()),
  path('student/create/upload/', StudentListUploadView.as_view()),
  path('faculty/create/upload/', FacultyListUploadView.as_view()),
  path('staff/create/upload/', StaffListUploadView.as_view()),
  path('user/student/register/', student_register),
  path('user/faculty/register/', faculty_register),
  path('user/staff/register/', staff_register),
  path('deactivate_user/', DeactivateUser.as_view(), name='deactivate_user'),
  path('deactivate_multiple_user/', DeactivateMultipleUser.as_view(), name='deactivate_multiple_user'),
  path('edit-profile/', EditProfileView.as_view()),
  path('send-log/', SendLogFileView.as_view(), name='send-log')
]