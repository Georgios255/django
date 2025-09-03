from django.core.management.base import BaseCommand
from faker import Faker
import random, datetime
from employees.models import Department, Employee, Performance
from attendance.models import Attendance

class Command(BaseCommand):
    help = "Seed fake departments, employees, attendance, performance"

    def add_arguments(self, parser):
        parser.add_argument("--employees", type=int, default=50)

    def handle(self, *args, **opts):
        fake = Faker()

        # Departments
        dept_names = ["Engineering", "HR", "Sales", "Finance", "Marketing", "Support"]
        departments = [Department.objects.get_or_create(name=n)[0] for n in dept_names]

        # Employees
        employees = []
        for _ in range(opts["employees"]):
            e = Employee.objects.create(
                name=fake.name(),
                email=fake.unique.email(),
                phone=fake.phone_number()[:20],
                address=fake.address(),
                date_of_joining=fake.date_between(start_date="-3y", end_date="today"),
                department=random.choice(departments),
            )
            employees.append(e)

        # Attendance for the last 60 days
        today = datetime.date.today()
        for e in employees:
            for d in range(0, 60):
                day = today - datetime.timedelta(days=d)
                status = random.choices(["P", "A", "L"], weights=[0.85, 0.1, 0.05])[0]
                Attendance.objects.get_or_create(employee=e, date=day, defaults={"status": status})

        # Performance reviews (2–4 per employee)
        for e in employees:
            for _ in range(random.randint(2, 4)):
                Performance.objects.create(
                    employee=e,
                    rating=random.randint(1, 5),
                    review_date=fake.date_between(start_date=e.date_of_joining, end_date="today"),
                )

        self.stdout.write(self.style.SUCCESS("Seeded data successfully"))