from django.urls import path
from .views import ParentRegistrationView, ParentProfileView, DemoStudentLoginView, StudentProfileView, StudentScheduleView, ScanLogView, CreateBusPassView, AdminScanLogView, StudentScheduleReportView, ParentChildrenListView, LinkChildView, ParentChildLogView, CustomTokenObtainPairView, CustomTokenRefreshView
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    path('parents/register/', ParentRegistrationView.as_view(), name='parent-register'),
    path('parents/me/', ParentProfileView.as_view(), name='parent-profile'),
    path('parents/me/children/', ParentChildrenListView.as_view(), name='parent-children-list'),
    path('parents/me/link-child/', LinkChildView.as_view(), name='parent-link-child'),
    path('parents/me/children/<str:university_id>/logs/', ParentChildLogView.as_view(), name='parent-child-logs'),
    
    path('students/demo-login/', DemoStudentLoginView.as_view(), name='demo-student-login'),
    path('students/me/', StudentProfileView.as_view(), name='student-profile'),
    path('students/schedule/', StudentScheduleView.as_view(), name='student-schedule'),
    path('logs/scan/', ScanLogView.as_view(), name='scan-log'),

    path('admin/bus-pass/create/', CreateBusPassView.as_view(), name='admin-create-pass'),
    path('admin/scan-logs/', AdminScanLogView.as_view(), name='admin-scan-logs'),
    path('admin/student-report/', StudentScheduleReportView.as_view(), name='admin-student-report')
]