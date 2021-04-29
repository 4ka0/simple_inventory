from django.urls import reverse
from django.test import TestCase

from ..models import Fruit
from users.models import CustomUser


class CreateViewTests(TestCase):
    def test_stock_create_view_redirection_when_not_logged_in(self):
        response = self.client.get(reverse("stock_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/stock/create/")

    def test_stock_create_view_when_logged_in(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stock_create"))
        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stock/stock_create.html")

    def test_stock_create_view_with_data(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        self.client.post(
            reverse("stock_create"), {"name": "apple", "price": 100}
        )
        self.assertEqual(Fruit.objects.last().name, "apple")
        self.assertEqual(Fruit.objects.last().price, 100)

    def test_stock_create_view_no_data(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stock_create"))
        self.assertContains(response, "New Stock")
        self.assertContains(response, "Name")
        self.assertContains(response, "Price")
        self.assertContains(response, "Cancel")
