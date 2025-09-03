from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from employees.views import DepartmentViewSet, EmployeeViewSet, PerformanceViewSet
from attendance.views import AttendanceViewSet

# JWT
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r"departments", DepartmentViewSet)
router.register(r"employees", EmployeeViewSet)
router.register(r"performances", PerformanceViewSet)
router.register(r"attendance", AttendanceViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title="Employee Management API",
        default_version="v1",
        description="APIs for Employees, Departments, Attendance, Performance",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # JWT auth endpoints (these are the ones you’re looking for)
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Swagger / ReDoc
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="redoc"),
]

from employees.analytics import EmployeesPerDepartment, MonthlyAttendance
from django.views.generic import TemplateView

urlpatterns += [
    path("api/analytics/employees-per-department/", EmployeesPerDepartment.as_view()),
    path("api/analytics/monthly-attendance/", MonthlyAttendance.as_view()),
    path("charts/", TemplateView.as_view(template_name="charts.html")),  # <-- this
]