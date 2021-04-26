from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from stock.models import Fruit
from users.models import CustomUser
from sales.models import Sale


class SaleDeleteViewTests(TestCase):
    def test_sale_delete_view(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        pineapple = Fruit.objects.create(name="pineapple", price=500)
        pineapple_sale = Sale.objects.create(
            fruit=pineapple, quantity=3, proceeds=1500, sold_on=timezone.now()
        )
        self.assertEqual(Sale.objects.count(), 1)
        post_response = self.client.post(
            reverse("sale_delete", args=(pineapple_sale.id,)), follow=True
        )
        self.assertRedirects(
            post_response, reverse("sale_list"), status_code=302
        )
        self.assertEqual(Sale.objects.count(), 0)
