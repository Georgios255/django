from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from employees.models import Department

class EmployeesApiSmokeTest(APITestCase):
    def setUp(self):
        # create a normal user for JWT auth
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass12345")

        # create at least one department so list/filters have data
        Department.objects.create(name="QA")

        # get a JWT access token
        res = self.client.post("/api/token/", {
            "username": "tester",
            "password": "pass12345"
        }, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK, res.data)
        access = res.data["access"]

        # attach Authorization header to all subsequent requests
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

    def test_list_departments(self):
        r = self.client.get("/api/departments/")
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        # if you use pagination, results may be in r.data["results"]
        results = r.data.get("results", r.data)
        self.assertGreaterEqual(len(results), 1)