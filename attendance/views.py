from rest_framework import viewsets, permissions
from django_filters.rest_framework import FilterSet, filters
from .models import Attendance
from .serializers import AttendanceSerializer

class AttendanceFilter(FilterSet):
    date = filters.DateFilter(field_name="date")
    status = filters.CharFilter(field_name="status")
    employee = filters.NumberFilter(field_name="employee_id")

    class Meta:
        model = Attendance
        fields = ["date", "status", "employee"]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related("employee").all()
    serializer_class = AttendanceSerializer
    filterset_class = AttendanceFilter
    ordering_fields = ["date", "employee"]
    permission_classes = [permissions.IsAuthenticated]