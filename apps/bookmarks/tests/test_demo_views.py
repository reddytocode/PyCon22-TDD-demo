
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class TestAddView(TestCase):
    def setUp(self):
        self.app = APIClient()
        self.url = reverse("bookmarks:add-endpoint")
        self.data = {"a": 2, "b": 2}

    def test_success(self):
        response = self.app.post(self.url, data=self.data)
        self.assertEqual(response.status_code, 200)