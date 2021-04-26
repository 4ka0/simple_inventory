import pytz
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone
from datetime import datetime

from stock.models import Fruit
from users.models import CustomUser
from sales.models import Sale


class SaleUpdateViewTests(TestCase):
    def test_sale_update_view_redirection_when_not_logged_in(self):
        fruit = Fruit.objects.create(name="apple", price=500)
        sale = Sale.objects.create(
            fruit=fruit, quantity=5, proceeds=2500, sold_on=timezone.now()
        )
        response = self.client.get(reverse("sale_update", args=[sale.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/accounts/login/?next=/sales/{sale.pk}/update/"
        )

    def test_sale_update_view_when_logged_in(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        fruit = Fruit.objects.create(name="apple", price=500)
        sale = Sale.objects.create(
            fruit=fruit, quantity=5, proceeds=2500, sold_on=timezone.now()
        )
        response = self.client.get(reverse("sale_update", args=[sale.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "sales/sale_update.html")

    def test_sale_update_view_new_quantity_and_date(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)

        lemon = Fruit.objects.create(name="lemon", price=100)
        lemon_sale = Sale.objects.create(
            fruit=lemon,
            fruit_price_when_sold=100,
            quantity=5,
            proceeds=500,
            sold_on=timezone.now(),
        )

        response = self.client.get(
            reverse("sale_update", args=[lemon_sale.pk])
        )
        form = response.context["form"]
        data = form.initial

        try:
            new_date_naive = datetime.strptime(
                "2000-01-01 12:00", "%Y-%m-%d %H:%M"
            )
        except ValueError as e:
            print(e)

        tz = pytz.timezone("Asia/Tokyo")
        new_date_aware = tz.localize(new_date_naive)

        data["sold_on"] = new_date_aware
        data["quantity"] = 10
        self.client.post(reverse("sale_update", args=[lemon_sale.pk]), data)

        lemon_sale = Sale.objects.get(id=lemon_sale.pk)
        self.assertEqual(lemon_sale.quantity, 10)
        self.assertEqual(lemon_sale.proceeds, 1000)
        self.assertEqual(lemon_sale.sold_on, new_date_aware)
