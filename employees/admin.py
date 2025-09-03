from django.contrib import admin
from .models import Department, Employee, Performance

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "department", "date_of_joining")
    search_fields = ("name", "email")
    list_filter = ("department",)

@admin.register(Performance)
class PerformanceAdmin(admin.ModelAdmin):
    list_display = ("id", "employee", "rating", "review_date")
    list_filter = ("rating",)