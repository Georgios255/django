from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from employees.models import Employee
from attendance.models import Attendance
from django.utils import timezone
from datetime import timedelta

class EmployeesPerDepartment(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        data = (Employee.objects.values("department__name")
                .annotate(total=Count("id")).order_by("department__name"))
        return Response({
            "labels": [d["department__name"] for d in data],
            "values": [d["total"] for d in data]
        })

class MonthlyAttendance(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        start = (timezone.now().date().replace(day=1) - timedelta(days=180))
        qs = (Attendance.objects.filter(date__gte=start)
              .values("date").annotate(total=Count("id")).order_by("date"))
        return Response({
            "labels": [str(r["date"]) for r in qs],
            "values": [r["total"] for r in qs]
        })