from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from stock.models import Fruit
from users.models import CustomUser
from sales.models import Sale

from freezegun import freeze_time


class SaleListViewTests(TestCase):
    def test_sale_list_view_redirection_when_not_logged_in(self):
        response = self.client.get(reverse("sale_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/sales/list/")

    def test_sale_list_view_when_logged_in(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("sale_list"))
        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)

    def test_sale_list_view_templates_used(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("sale_list"))
        self.assertTemplateUsed(response, "sales/sale_list.html")
        self.assertTemplateUsed(response, "base.html")

    @freeze_time("2021-06-01")
    def test_sale_list_view_context(self):

        # 果物オブジェクトを作成する
        apple = Fruit.objects.create(name="apple", price=100)
        lemon = Fruit.objects.create(name="lemon", price=200)
        orange = Fruit.objects.create(name="orange", price=300)

        # 販売オブジェクトを作成する
        sale1 = Sale.objects.create(
            fruit=apple,
            quantity=2,
            fruit_price_when_sold=100,
            proceeds=200,
            sold_on=timezone.now(),
        )
        sale2 = Sale.objects.create(
            fruit=lemon,
            quantity=2,
            fruit_price_when_sold=200,
            proceeds=400,
            sold_on=timezone.now(),
        )
        sale3 = Sale.objects.create(
            fruit=orange,
            quantity=2,
            fruit_price_when_sold=300,
            proceeds=600,
            sold_on=timezone.now(),
        )

        # ログインしてレスポンスを得る
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("sale_list"))

        # コンテクストを確認する

        sales = response.context["sales"]
        self.assertEqual(len(sales), 3)
        self.assertIsInstance(response.context["sales"][0], Sale)
        self.assertIsInstance(response.context["sales"][1], Sale)
        self.assertIsInstance(response.context["sales"][2], Sale)

        sale1 = sales[0]
        sale2 = sales[1]
        sale3 = sales[2]

        self.assertEqual(sale1.fruit, apple)
        self.assertEqual(sale1.fruit_name, "apple")
        self.assertEqual(sale1.quantity, 2)
        self.assertEqual(sale1.fruit_price_when_sold, 100)
        self.assertEqual(sale1.proceeds, 200)
        self.assertEqual(str(sale1.sold_on), "2021-06-01 00:00:00+00:00")

        self.assertEqual(sale2.fruit, lemon)
        self.assertEqual(sale2.fruit_name, "lemon")
        self.assertEqual(sale2.quantity, 2)
        self.assertEqual(sale2.fruit_price_when_sold, 200)
        self.assertEqual(sale2.proceeds, 400)
        self.assertEqual(str(sale2.sold_on), "2021-06-01 00:00:00+00:00")

        self.assertEqual(sale3.fruit, orange)
        self.assertEqual(sale3.fruit_name, "orange")
        self.assertEqual(sale3.quantity, 2)
        self.assertEqual(sale3.fruit_price_when_sold, 300)
        self.assertEqual(sale3.proceeds, 600)
        self.assertEqual(str(sale3.sold_on), "2021-06-01 00:00:00+00:00")

    def test_sale_list_view_context_display_order(self):

        # 果物オブジェクトを作成する
        fruit1 = Fruit.objects.create(name="リンゴ", price=100)
        fruit2 = Fruit.objects.create(name="レモン", price=200)
        fruit3 = Fruit.objects.create(name="オレンジ", price=300)

        # 販売オブジェクトを作成する
        Sale.objects.create(
            fruit=fruit1, quantity=2, proceeds=200, sold_on=timezone.now()
        )
        Sale.objects.create(
            fruit=fruit2, quantity=2, proceeds=400, sold_on=timezone.now()
        )
        Sale.objects.create(
            fruit=fruit3, quantity=2, proceeds=600, sold_on=timezone.now()
        )

        # ログインする
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)

        # 元々のコンテクストの順番を確認する
        # 直近で販売されたものから順に並べているはずです
        response = self.client.get(reverse("sale_list"))
        self.assertEqual(response.context["sales"][0].fruit_name, "オレンジ")
        self.assertEqual(response.context["sales"][1].fruit_name, "レモン")
        self.assertEqual(response.context["sales"][2].fruit_name, "リンゴ")
