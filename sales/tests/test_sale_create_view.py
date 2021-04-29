from datetime import datetime
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from stock.models import Fruit
from users.models import CustomUser
from sales.models import Sale

from freezegun import freeze_time


class SaleCreateViewTests(TestCase):
    def test_sale_create_view_redirection_when_not_logged_in(self):
        response = self.client.get(reverse("sale_create"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/sales/create/")

    def test_sale_create_view_when_logged_in(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("sale_create"))
        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/sale_create.html")

    def test_sale_create_view_with_data(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        apple = Fruit.objects.create(name="apple", price=100)
        self.client.post(
            reverse("sale_create"),
            {"fruit": apple.id, "quantity": 10, "sold_on": timezone.now()},
        )
        self.assertEqual(Sale.objects.last().fruit_name, "apple")
        self.assertEqual(Sale.objects.last().quantity, 10)
        self.assertEqual(Sale.objects.last().proceeds, 1000)

    def test_sale_create_view_no_data(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("sale_create"))
        self.assertContains(response, "New Sale")
        self.assertContains(response, "Fruit")
        self.assertContains(response, "Quantity")
        self.assertContains(response, "Cancel")

    @freeze_time("2021-01-01")
    def test_sale_create_view_doesnt_accept_duplicate_data(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        apple = Fruit.objects.create(name="apple", price=100)
        self.client.post(
            reverse("sale_create"),
            {"fruit": apple.id, "quantity": 10, "sold_on": timezone.now()},
        )
        self.client.post(
            reverse("sale_create"),
            {"fruit": apple.id, "quantity": 10, "sold_on": timezone.now()},
        )
        self.assertEqual(Sale.objects.count(), 1)

    @freeze_time("2021-01-01 00:00")
    def test_sale_create_view_time_edge_case(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        apple = Fruit.objects.create(name="apple", price=100)
        self.client.post(
            reverse("sale_create"),
            {"fruit": apple.id, "quantity": 5, "sold_on": timezone.now()},
        )
        expected = datetime(year=2021, month=1, day=1, hour=0, minute=0)
        self.assertEqual(
            Sale.objects.last().sold_on.replace(tzinfo=None),
            expected
        )
