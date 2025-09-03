from rest_framework import viewsets, permissions
from django_filters.rest_framework import FilterSet, filters
from .models import Department, Employee, Performance
from .serializers import DepartmentSerializer, EmployeeSerializer, PerformanceSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().order_by("name")
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmployeeFilter(FilterSet):
    department = filters.NumberFilter(field_name="department_id")
    joined_after = filters.DateFilter(field_name="date_of_joining", lookup_expr="gte")
    joined_before = filters.DateFilter(field_name="date_of_joining", lookup_expr="lte")

    class Meta:
        model = Employee
        fields = ["department", "joined_after", "joined_before"]

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.select_related("department").all()
    serializer_class = EmployeeSerializer
    filterset_class = EmployeeFilter
    search_fields = ["name", "email"]
    ordering_fields = ["name", "date_of_joining"]
    permission_classes = [permissions.IsAuthenticated]

class PerformanceViewSet(viewsets.ModelViewSet):
    queryset = Performance.objects.select_related("employee").all()
    serializer_class = PerformanceSerializer
    permission_classes = [permissions.IsAuthenticated]