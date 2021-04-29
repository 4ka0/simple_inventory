from django.urls import reverse
from django.test import TestCase

from ..models import Fruit
from users.models import CustomUser

from freezegun import freeze_time


class ListViewTests(TestCase):
    def test_stock_list_view_redirection_when_not_logged_in(self):
        response = self.client.get(reverse("stock_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/stock/list/")

    def test_stock_list_view_when_logged_in(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stock_list"))
        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)

    def test_stock_list_view_templates_used(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stock_list"))
        self.assertTemplateUsed(response, "base.html")
        self.assertTemplateUsed(response, "stock/stock_list.html")

    @freeze_time("2021-04-03")
    def test_stock_list_view_context(self):

        # 果物オブジェクトを作成する
        fruit1 = Fruit.objects.create(name="apple", price=100)
        fruit2 = Fruit.objects.create(name="lemon", price=200)
        fruit3 = Fruit.objects.create(name="orange", price=300)

        # ログインしてレスポンスを得る
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stock_list"))

        # コンテクストを確認する

        fruits = response.context["fruits"]
        self.assertEqual(len(fruits), 3)
        self.assertIsInstance(response.context["fruits"][0], Fruit)
        self.assertIsInstance(response.context["fruits"][1], Fruit)
        self.assertIsInstance(response.context["fruits"][2], Fruit)

        fruit1 = fruits[0]
        fruit2 = fruits[1]
        fruit3 = fruits[2]

        self.assertEqual(fruit1.name, "apple")
        self.assertEqual(fruit1.price, 100)
        self.assertEqual(str(fruit1.created_on), "2021-04-03 00:00:00+00:00")
        self.assertEqual(str(fruit1.updated_on), "2021-04-03 00:00:00+00:00")

        self.assertEqual(fruit2.name, "lemon")
        self.assertEqual(fruit2.price, 200)
        self.assertEqual(str(fruit2.created_on), "2021-04-03 00:00:00+00:00")
        self.assertEqual(str(fruit2.updated_on), "2021-04-03 00:00:00+00:00")

        self.assertEqual(fruit3.name, "orange")
        self.assertEqual(fruit3.price, 300)
        self.assertEqual(str(fruit3.created_on), "2021-04-03 00:00:00+00:00")
        self.assertEqual(str(fruit3.updated_on), "2021-04-03 00:00:00+00:00")

    def test_stock_list_view_context_display_order(self):

        # 果物オブジェクトを作成する
        Fruit.objects.create(name="リンゴ", price=100)
        Fruit.objects.create(name="レモン", price=200)
        fruit = Fruit.objects.create(name="オレンジ", price=300)

        # ログインする
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)

        # 元々のコンテクストの順番を確認する
        # 新しいものから順に並べているはずです
        response = self.client.get(reverse("stock_list"))
        self.assertEqual(response.context["fruits"][0].name, "オレンジ")
        self.assertEqual(response.context["fruits"][1].name, "レモン")
        self.assertEqual(response.context["fruits"][2].name, "リンゴ")

        # 一つのオブジェクトを更新してコンテクストの新しい順番を確認する
        # 更新されたものが最初に並べているはずです
        fruit.price = 1000
        fruit.save()
        response = self.client.get(reverse("stock_list"))
        self.assertEqual(response.context["fruits"][0].name, "オレンジ")
        self.assertEqual(response.context["fruits"][1].name, "レモン")
        self.assertEqual(response.context["fruits"][2].name, "リンゴ")
