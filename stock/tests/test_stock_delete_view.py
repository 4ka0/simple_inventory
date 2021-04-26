from django.urls import reverse
from django.test import TestCase

from .models import Fruit
from users.models import CustomUser


class DeleteViewTests(TestCase):
    def test_stock_delete_view(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        fruit = Fruit.objects.create(name="pineapple", price=1800)
        self.assertEqual(Fruit.objects.count(), 1)
        post_response = self.client.post(
            reverse("stock_delete", args=(fruit.id,)), follow=True
        )
        self.assertRedirects(
            post_response, reverse("stock_list"), status_code=302
        )
        self.assertEqual(Fruit.objects.count(), 0)
