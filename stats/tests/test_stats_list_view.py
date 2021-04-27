import pytz
from datetime import datetime
import dateutil.relativedelta
from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from users.models import CustomUser
from stock.models import Fruit
from sales.models import Sale
from .views import (
    get_total_proceeds,
    get_sales_for_period,
    sort_sales_by_day,
    sort_sales_by_month,
    build_sales_details,
)

from freezegun import freeze_time


class StatsListTests(TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.apple = Fruit.objects.create(name="apple", price=100)
        cls.lemon = Fruit.objects.create(name="lemon", price=120)
        cls.orange = Fruit.objects.create(name="orange", price=140)
        cls.kiwi = Fruit.objects.create(name="kiwi", price=160)
        cls.banana = Fruit.objects.create(name="banana", price=180)

        # 1日目、1ヶ月目
        with freeze_time("2020-04-15"):
            cls.sale1 = Sale.objects.create(
                fruit=cls.apple,
                quantity=1,
                fruit_price_when_sold=100,
                proceeds=100,
                sold_on=timezone.now(),
            )
            cls.sale2 = Sale.objects.create(
                fruit=cls.lemon,
                quantity=2,
                fruit_price_when_sold=120,
                proceeds=240,
                sold_on=timezone.now(),
            )
            cls.sale3 = Sale.objects.create(
                fruit=cls.orange,
                quantity=3,
                fruit_price_when_sold=140,
                proceeds=420,
                sold_on=timezone.now(),
            )
            cls.sale4 = Sale.objects.create(
                fruit=cls.kiwi,
                quantity=4,
                fruit_price_when_sold=160,
                proceeds=640,
                sold_on=timezone.now(),
            )
            cls.sale5 = Sale.objects.create(
                fruit=cls.banana,
                quantity=5,
                fruit_price_when_sold=180,
                proceeds=900,
                sold_on=timezone.now(),
            )

        # 2日目、1ヶ月目
        with freeze_time("2020-04-16"):
            cls.sale6 = Sale.objects.create(
                fruit=cls.apple,
                quantity=1,
                fruit_price_when_sold=100,
                proceeds=100,
                sold_on=timezone.now(),
            )
            cls.sale7 = Sale.objects.create(
                fruit=cls.lemon,
                quantity=2,
                fruit_price_when_sold=120,
                proceeds=240,
                sold_on=timezone.now(),
            )
            cls.sale8 = Sale.objects.create(
                fruit=cls.orange,
                quantity=3,
                fruit_price_when_sold=140,
                proceeds=420,
                sold_on=timezone.now(),
            )
            cls.sale9 = Sale.objects.create(
                fruit=cls.kiwi,
                quantity=4,
                fruit_price_when_sold=160,
                proceeds=640,
                sold_on=timezone.now(),
            )
            cls.sale10 = Sale.objects.create(
                fruit=cls.banana,
                quantity=5,
                fruit_price_when_sold=180,
                proceeds=900,
                sold_on=timezone.now(),
            )

        # 3日目、1ヶ月目
        with freeze_time("2020-04-17"):
            cls.sale11 = Sale.objects.create(
                fruit=cls.apple,
                quantity=1,
                fruit_price_when_sold=100,
                proceeds=100,
                sold_on=timezone.now(),
            )
            cls.sale12 = Sale.objects.create(
                fruit=cls.lemon,
                quantity=2,
                fruit_price_when_sold=120,
                proceeds=240,
                sold_on=timezone.now(),
            )
            cls.sale13 = Sale.objects.create(
                fruit=cls.orange,
                quantity=3,
                fruit_price_when_sold=140,
                proceeds=420,
                sold_on=timezone.now(),
            )
            cls.sale14 = Sale.objects.create(
                fruit=cls.kiwi,
                quantity=4,
                fruit_price_when_sold=160,
                proceeds=640,
                sold_on=timezone.now(),
            )
            cls.sale15 = Sale.objects.create(
                fruit=cls.banana,
                quantity=5,
                fruit_price_when_sold=180,
                proceeds=900,
                sold_on=timezone.now(),
            )

        # 2ヶ月目
        with freeze_time("2020-03-20"):
            cls.sale16 = Sale.objects.create(
                fruit=cls.apple,
                quantity=1,
                fruit_price_when_sold=100,
                proceeds=100,
                sold_on=timezone.now(),
            )
            cls.sale17 = Sale.objects.create(
                fruit=cls.lemon,
                quantity=2,
                fruit_price_when_sold=120,
                proceeds=240,
                sold_on=timezone.now(),
            )
            cls.sale18 = Sale.objects.create(
                fruit=cls.orange,
                quantity=3,
                fruit_price_when_sold=140,
                proceeds=420,
                sold_on=timezone.now(),
            )
            cls.sale19 = Sale.objects.create(
                fruit=cls.kiwi,
                quantity=4,
                fruit_price_when_sold=160,
                proceeds=640,
                sold_on=timezone.now(),
            )
            cls.sale20 = Sale.objects.create(
                fruit=cls.banana,
                quantity=5,
                fruit_price_when_sold=180,
                proceeds=900,
                sold_on=timezone.now(),
            )
            cls.sale21 = Sale.objects.create(
                fruit=cls.apple,
                quantity=1,
                fruit_price_when_sold=100,
                proceeds=100,
                sold_on=timezone.now(),
            )
            cls.sale22 = Sale.objects.create(
                fruit=cls.lemon,
                quantity=2,
                fruit_price_when_sold=120,
                proceeds=240,
                sold_on=timezone.now(),
            )
            cls.sale23 = Sale.objects.create(
                fruit=cls.orange,
                quantity=3,
                fruit_price_when_sold=140,
                proceeds=420,
                sold_on=timezone.now(),
            )
            cls.sale24 = Sale.objects.create(
                fruit=cls.kiwi,
                quantity=4,
                fruit_price_when_sold=160,
                proceeds=640,
                sold_on=timezone.now(),
            )
            cls.sale25 = Sale.objects.create(
                fruit=cls.banana,
                quantity=5,
                fruit_price_when_sold=180,
                proceeds=900,
                sold_on=timezone.now(),
            )

        # 3ヶ月目
        with freeze_time("2020-02-20"):
            cls.sale26 = Sale.objects.create(
                fruit=cls.apple,
                quantity=1,
                fruit_price_when_sold=100,
                proceeds=100,
                sold_on=timezone.now(),
            )
            cls.sale27 = Sale.objects.create(
                fruit=cls.lemon,
                quantity=2,
                fruit_price_when_sold=120,
                proceeds=240,
                sold_on=timezone.now(),
            )
            cls.sale28 = Sale.objects.create(
                fruit=cls.orange,
                quantity=3,
                fruit_price_when_sold=140,
                proceeds=420,
                sold_on=timezone.now(),
            )
            cls.sale29 = Sale.objects.create(
                fruit=cls.kiwi,
                quantity=4,
                fruit_price_when_sold=160,
                proceeds=640,
                sold_on=timezone.now(),
            )
            cls.sale30 = Sale.objects.create(
                fruit=cls.banana,
                quantity=5,
                fruit_price_when_sold=180,
                proceeds=900,
                sold_on=timezone.now(),
            )
            cls.sale31 = Sale.objects.create(
                fruit=cls.apple,
                quantity=1,
                fruit_price_when_sold=100,
                proceeds=100,
                sold_on=timezone.now(),
            )
            cls.sale32 = Sale.objects.create(
                fruit=cls.lemon,
                quantity=2,
                fruit_price_when_sold=120,
                proceeds=240,
                sold_on=timezone.now(),
            )
            cls.sale33 = Sale.objects.create(
                fruit=cls.orange,
                quantity=3,
                fruit_price_when_sold=140,
                proceeds=420,
                sold_on=timezone.now(),
            )
            cls.sale34 = Sale.objects.create(
                fruit=cls.kiwi,
                quantity=4,
                fruit_price_when_sold=160,
                proceeds=640,
                sold_on=timezone.now(),
            )
            cls.sale35 = Sale.objects.create(
                fruit=cls.banana,
                quantity=5,
                fruit_price_when_sold=180,
                proceeds=900,
                sold_on=timezone.now(),
            )

        # 4ヶ月目
        with freeze_time("2020-01-20"):
            cls.sale36 = Sale.objects.create(
                fruit=cls.apple,
                quantity=1,
                fruit_price_when_sold=100,
                proceeds=100,
                sold_on=timezone.now(),
            )
            cls.sale37 = Sale.objects.create(
                fruit=cls.lemon,
                quantity=2,
                fruit_price_when_sold=120,
                proceeds=240,
                sold_on=timezone.now(),
            )
            cls.sale38 = Sale.objects.create(
                fruit=cls.orange,
                quantity=3,
                fruit_price_when_sold=140,
                proceeds=420,
                sold_on=timezone.now(),
            )
            cls.sale39 = Sale.objects.create(
                fruit=cls.kiwi,
                quantity=4,
                fruit_price_when_sold=160,
                proceeds=640,
                sold_on=timezone.now(),
            )
            cls.sale40 = Sale.objects.create(
                fruit=cls.banana,
                quantity=5,
                fruit_price_when_sold=180,
                proceeds=900,
                sold_on=timezone.now(),
            )

        cls.sales = [
            cls.sale1,
            cls.sale2,
            cls.sale3,
            cls.sale4,
            cls.sale5,
            cls.sale6,
            cls.sale7,
            cls.sale8,
            cls.sale9,
            cls.sale10,
            cls.sale11,
            cls.sale12,
            cls.sale13,
            cls.sale14,
            cls.sale15,
            cls.sale16,
            cls.sale17,
            cls.sale18,
            cls.sale19,
            cls.sale20,
            cls.sale21,
            cls.sale22,
            cls.sale23,
            cls.sale24,
            cls.sale25,
            cls.sale26,
            cls.sale27,
            cls.sale28,
            cls.sale29,
            cls.sale30,
            cls.sale31,
            cls.sale32,
            cls.sale33,
            cls.sale34,
            cls.sale35,
            cls.sale36,
            cls.sale37,
            cls.sale38,
            cls.sale39,
            cls.sale40,
        ]

    # ヘルパー関数のテスト

    def test_total_proceeds_calculated_correctly(self):
        self.assertEqual(get_total_proceeds(self.sales), 18400)
        self.assertNotEqual(get_total_proceeds(self.sales), 0)

    @freeze_time("2020-04-17")
    def test_get_sales_for_period_days(self):
        sales = get_sales_for_period(self.sales, "days")
        self.assertEqual(len(sales), 15)
        three_days_ago = timezone.now() - dateutil.relativedelta.relativedelta(
            days=3
        )
        for sale in sales:
            self.assertTrue(sale.sold_on >= three_days_ago)

    @freeze_time("2020-04-17")
    def test_get_sales_for_period_months(self):
        sales = get_sales_for_period(self.sales, "months")
        self.assertEqual(len(sales), 35)
        start_day = timezone.now() - dateutil.relativedelta.relativedelta(
            days=16, months=2
        )
        for sale in sales:
            self.assertTrue(sale.sold_on >= start_day)

    @freeze_time("2020-04-17")
    def test_sort_sales_by_day(self):
        day_sales = get_sales_for_period(self.sales, "days")
        sorted_sales = sort_sales_by_day(day_sales)
        # 各行の日付を確認する
        self.assertEqual(
            sorted_sales[0].date, datetime(year=2020, month=4, day=17).date()
        )
        self.assertEqual(
            sorted_sales[1].date, datetime(year=2020, month=4, day=16).date()
        )
        self.assertEqual(
            sorted_sales[2].date, datetime(year=2020, month=4, day=15).date()
        )
        # 各saleの日付がその行の日付と一致することを確認する
        for row in sorted_sales:
            for sale in row.sales:
                # 比較できるように、naiveなdatetimeオブジェクトに変換する
                sale_date = sale.sold_on.replace(tzinfo=None).date()
                self.assertEqual(row.date, sale_date)

    @freeze_time("2020-04-17")
    def test_sort_sales_by_month(self):
        month_sales = get_sales_for_period(self.sales, "months")
        sorted_sales = sort_sales_by_month(month_sales)
        # 各行の日付を確認する
        self.assertEqual(
            sorted_sales[0].date,
            datetime(year=2020, month=4, day=1, tzinfo=pytz.UTC),
        )
        self.assertEqual(
            sorted_sales[1].date,
            datetime(year=2020, month=3, day=1, tzinfo=pytz.UTC),
        )
        self.assertEqual(
            sorted_sales[2].date,
            datetime(year=2020, month=2, day=1, tzinfo=pytz.UTC),
        )
        # 各saleの日付がその行の日付範囲に一致することを確認する
        for row in sorted_sales:
            for sale in row.sales:
                # 対応する日付範囲の境界値を取得する
                lower_bound = row.date
                upper_bound = (
                    lower_bound + dateutil.relativedelta.relativedelta(day=31)
                )
                # 比較できるように、naiveなdatetimeオブジェクトに変換する
                lower_bound = lower_bound.replace(tzinfo=pytz.UTC)
                upper_bound = upper_bound.replace(tzinfo=pytz.UTC)
                self.assertTrue(sale.sold_on >= lower_bound)
                self.assertTrue(sale.sold_on < upper_bound)

    @freeze_time("2020-04-17")
    def test_build_sales_details_by_day(self):
        day_sales = get_sales_for_period(self.sales, "days")
        sorted_sales = sort_sales_by_day(day_sales)
        day_sales_with_bd = build_sales_details(sorted_sales)
        self.assertEqual(
            sorted_sales[0].details_str,
            "banana: 900円 (5), kiwi: 640円 (4), orange: 420円 (3), lemon: 240円 (2), apple: 100円 (1)",
        )
        self.assertEqual(
            sorted_sales[1].details_str,
            "banana: 900円 (5), kiwi: 640円 (4), orange: 420円 (3), lemon: 240円 (2), apple: 100円 (1)",
        )
        self.assertEqual(
            sorted_sales[2].details_str,
            "banana: 900円 (5), kiwi: 640円 (4), orange: 420円 (3), lemon: 240円 (2), apple: 100円 (1)",
        )

    @freeze_time("2020-04-17")
    def test_build_sales_details_by_month(self):
        month_sales = get_sales_for_period(self.sales, "months")
        sorted_sales = sort_sales_by_month(month_sales)
        month_sales_with_bd = build_sales_details(sorted_sales)
        self.assertEqual(
            sorted_sales[0].details_str,
            "banana: 2700円 (15), kiwi: 1920円 (12), orange: 1260円 (9), lemon: 720円 (6), apple: 300円 (3)",
        )
        self.assertEqual(
            sorted_sales[1].details_str,
            "banana: 1800円 (10), kiwi: 1280円 (8), orange: 840円 (6), lemon: 480円 (4), apple: 200円 (2)",
        )
        self.assertEqual(
            sorted_sales[2].details_str,
            "banana: 1800円 (10), kiwi: 1280円 (8), orange: 840円 (6), lemon: 480円 (4), apple: 200円 (2)",
        )

    # viewのテスト

    def test_stats_list_view_redirection_when_not_logged_in(self):
        response = self.client.get(reverse("stats_list"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/stats/list/")

    def test_stats_list_view_resolves_when_logged_in(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stats_list"))
        self.assertEqual(str(response.context["user"]), "testuser")
        self.assertEqual(response.status_code, 200)

    def test_stats_list_view_ues_correct_templates(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stats_list"))
        self.assertTemplateUsed(response, "stats/stats_list.html")
        self.assertTemplateUsed(response, "base.html")

    def test_stats_list_view_context_content(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stats_list"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total_proceeds", response.context)
        self.assertIn("month_sales", response.context)
        self.assertTrue(len(response.context["month_sales"]) == 3)
        self.assertIn("day_sales", response.context)
        self.assertTrue(len(response.context["day_sales"]) == 3)

    def test_stats_list_view_template_display(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("stats_list"))
        self.assertContains(response, "<h4>販売統計管理</h4>", 1)
        self.assertContains(response, "<h5>累計</h5>", 1)
        self.assertContains(response, "<h5>月別</h5>", 1)
        self.assertContains(response, "売り上げ</th>", 2)
        self.assertContains(response, "内訳</th>", 2)
