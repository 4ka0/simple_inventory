from django.urls import reverse
from django.test import TestCase

from .models import Fruit
from users.models import CustomUser


class UpdateViewTests(TestCase):
    def test_stock_update_view_redirection_when_not_logged_in(self):
        fruit = Fruit.objects.create(name="apple", price=500)
        response = self.client.get(reverse("stock_update", args=[fruit.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"/accounts/login/?next=/stock/{fruit.pk}/update/"
        )

    def test_stock_update_view_when_logged_in(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        fruit = Fruit.objects.create(name="apple", price=500)
        response = self.client.get(reverse("stock_update", args=[fruit.pk]))
        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "stock/stock_update.html")

    def test_stock_update_view(self):
        # ログインする
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        # 果物オブジェクトを作成する
        fruit = Fruit.objects.create(name="apple", price=100)
        # アップデートURLに送信する
        update_url = reverse("stock_update", args=[fruit.pk])
        response = self.client.get(update_url)
        # フォームデータを取得する
        form = response.context["form"]
        data = form.initial
        # データを更新する
        data["name"] = "lemon"
        data["price"] = 200
        # フォームへPOSTする
        self.client.post(update_url, data)
        # データの更新を確認する
        fruit = Fruit.objects.get(id=1)
        self.assertEqual(fruit.name, "lemon")
        self.assertNotEqual(fruit.name, "apple")
        self.assertEqual(fruit.price, 200)
        self.assertNotEqual(fruit.price, 100)
