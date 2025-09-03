from django.db import models

class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    def __str__(self): return self.name

class Employee(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_joining = models.DateField()
    department = models.ForeignKey(Department, related_name="employees",
                                   on_delete=models.CASCADE)
    def __str__(self): return f"{self.name} ({self.department})"

class Performance(models.Model):
    employee = models.ForeignKey(Employee, related_name="performances",
                                 on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review_date = models.DateField()
    def __str__(self): return f"{self.employee} - {self.rating}"