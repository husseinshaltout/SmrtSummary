from django.test import TestCase, Client
from django.urls import reverse


class ApiTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)

    def test_register_and_login(self):
        register_response = self.client.post(
            "/api/auth/register",
            {
                "firstname": "A",
                "lastname": "B",
                "username": "apiuser",
                "email": "api@example.com",
                "password": "securepass123",
                "password2": "securepass123",
            },
            content_type="application/json",
        )
        self.assertEqual(register_response.status_code, 201)
        login_response = self.client.post(
            "/api/auth/login",
            {"username": "apiuser", "password": "securepass123"},
            content_type="application/json",
        )
        self.assertEqual(login_response.status_code, 200)
        me_response = self.client.get("/api/auth/me")
        self.assertEqual(me_response.status_code, 200)
        self.assertEqual(me_response.json()["username"], "apiuser")
