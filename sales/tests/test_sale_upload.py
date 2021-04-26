import os
from django.urls import reverse
from django.test import TestCase

from stock.models import Fruit
from users.models import CustomUser
from sales.models import Sale, CsvUploadFile
from sales.forms import CsvUploadForm
from sales.views import generate_sale_objects, convert_str_to_tz_aware_datetime


class SaleUploadTests(TestCase):
    def setUp(self):
        Fruit.objects.create(name="apple", price=90)
        Fruit.objects.create(name="lemon", price=100)
        Fruit.objects.create(name="orange", price=110)

    def test_sale_upload_view_redirection_when_not_logged_in(self):
        with open("sales/tests/test_sales.csv", "r") as csv_file:
            response = self.client.post(
                reverse("sale_upload"), {"file_name": csv_file}
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/accounts/login/?next=/sales/upload/")

    def test_sale_upload_view_when_logged_in(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        with open("sales/tests/test_sales.csv", "r") as csv_file:
            response = self.client.post(
                reverse("sale_upload"), {"file_name": csv_file}
            )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, "/sales/list/")

    def test_successful_conversion_from_csv_to_sale_objects(self):
        csv_content = [
            ["apple", "3", "270", "2021-02-01 10:00"],
            ["lemon", "4", "400", "2021-02-02 10:05"],
            ["orange", "5", "550", "2021-02-03 10:10"],
        ]
        generate_sale_objects(csv_content)
        self.assertTrue(
            Sale.objects.filter(
                fruit_name="apple", quantity=3, proceeds=270
            ).exists()
        )
        self.assertTrue(
            Sale.objects.filter(
                fruit_name="lemon", quantity=4, proceeds=400
            ).exists()
        )
        self.assertTrue(
            Sale.objects.filter(
                fruit_name="orange", quantity=5, proceeds=550
            ).exists()
        )

    def test_convert_str_to_tz_aware_datetime(self):
        datetime_str = "2016-06-06 00:00"
        expected = "2016-06-06 00:00:00+09:00"
        datetime_obj = convert_str_to_tz_aware_datetime(datetime_str)
        self.assertEqual(str(datetime_obj), expected)

    def test_input_fails_with_incorrect_elem_number_in_row(self):
        csv_content = [
            ["apple", "3", "270"],
            ["lemon", "4", "170", "2021-02-01 10:00", "extra element"],
        ]
        generate_sale_objects(csv_content)
        self.assertFalse(
            Sale.objects.filter(
                fruit_name="apple", quantity=3, proceeds=270
            ).exists()
        )
        self.assertFalse(
            Sale.objects.filter(
                fruit_name="lemon", quantity=4, proceeds=170
            ).exists()
        )

    def test_input_fails_without_corresponding_fruit_object(self):
        csv_content = [
            ["banana", "4", "170", "2021-02-01 10:00"],
            ["pineapple", "4", "170", "2021-02-01 10:00"],
        ]
        generate_sale_objects(csv_content)
        self.assertFalse(
            Sale.objects.filter(
                fruit_name="banana", quantity=4, proceeds=170
            ).exists()
        )
        self.assertFalse(
            Sale.objects.filter(
                fruit_name="pineapple", quantity=4, proceeds=170
            ).exists()
        )

    def test_input_fails_with_non_digits_for_quantity_and_proceeds(self):
        csv_content = [
            ["apple", "three", "270", "2021-02-01 10:00"],
            ["lemon", "4", "one hundred", "2021-02-01 10:00"],
        ]
        generate_sale_objects(csv_content)
        self.assertFalse(
            Sale.objects.filter(fruit_name="apple", proceeds=270).exists()
        )
        self.assertFalse(
            Sale.objects.filter(fruit_name="lemon", quantity=4).exists()
        )

    def test_input_fails_if_time_not_in_correct_format(self):
        csv_content = [
            ["apple", "4", "170", "2021-2-1 10:00"],
            ["lemon", "4", "170", "2021-02-01 8:00"],
        ]
        generate_sale_objects(csv_content)
        self.assertFalse(
            Sale.objects.filter(
                fruit_name="apple", quantity=4, proceeds=170
            ).exists()
        )
        self.assertFalse(
            Sale.objects.filter(
                fruit_name="lemon", quantity=4, proceeds=170
            ).exists()
        )

    def test_input_fails_if_time_is_in_the_future(self):
        csv_content = [
            ["apple", "4", "170", "2022-06-01 10:00"],
            ["lemon", "4", "170", "2021-05-01 08:00"],
        ]
        generate_sale_objects(csv_content)
        self.assertFalse(
            Sale.objects.filter(
                fruit_name="apple", quantity=4, proceeds=170
            ).exists()
        )
        self.assertFalse(
            Sale.objects.filter(
                fruit_name="lemon", quantity=4, proceeds=170
            ).exists()
        )

    def test_input_fails_if_identical_sales_record_already_exists(self):
        banana = Fruit.objects.create(name="banana", price=100)
        pineapple = Fruit.objects.create(name="pineapple", price=200)
        datetime_obj = convert_str_to_tz_aware_datetime("2021-04-01 00:00")
        Sale.objects.create(
            fruit=banana, quantity=2, proceeds=200, sold_on=datetime_obj
        )
        Sale.objects.create(
            fruit=pineapple, quantity=2, proceeds=400, sold_on=datetime_obj
        )
        csv_content = [
            ["banana", "2", "200", "2021-04-01 00:00"],
            ["pineapple", "2", "400", "2021-04-01 00:00"],
        ]
        generate_sale_objects(csv_content)
        self.assertEqual(Sale.objects.count(), 2)

    def test_template_display_data_after_conversion_to_sale_objects(self):
        csv_content = [
            ["apple", "3", "270", "2000-01-01 12:00"],
            ["lemon", "4", "400", "2021-02-02 10:05"],
            ["orange", "5", "550", "2021-02-03 10:10"],
        ]
        generate_sale_objects(csv_content)

        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("sale_list"))

        self.assertContains(response, "apple", 1)
        self.assertContains(response, "270", 1)
        self.assertContains(response, "2000-01-01, 12:00", 1)

        self.assertContains(response, "lemon", 1)
        self.assertContains(response, "400", 1)
        self.assertContains(response, "2021-02-02, 10:05", 1)

        self.assertContains(response, "orange", 1)
        self.assertContains(response, "550", 1)
        self.assertContains(response, "2021-02-03, 10:10", 1)

    def test_duplicates_ignored_in_upload_of_multiple_identical_records(self):
        csv_content = [
            ["lemon", "2", "200", "2020-04-01 00:00"],
            ["lemon", "2", "200", "2020-04-01 00:00"],
            ["lemon", "2", "200", "2020-04-01 00:00"],
            ["lemon", "2", "200", "2020-04-01 00:00"],
            ["lemon", "2", "200", "2020-04-01 00:00"],
        ]
        generate_sale_objects(csv_content)
        self.assertEqual(Sale.objects.count(), 1)

    def test_sale_upload_with_data_from_file(self):

        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)

        Fruit.objects.create(name="レモン", price=100)
        Fruit.objects.create(name="ブルーベリー", price=100)
        Fruit.objects.create(name="グレープフルーツ", price=100)
        Fruit.objects.create(name="パイナップル", price=100)
        Fruit.objects.create(name="リンゴ", price=100)

        with open("sales/tests/test_sales.csv", "r") as csv_file:
            self.client.post(reverse("sale_upload"), {"file_name": csv_file})

        self.assertEqual(Sale.objects.count(), 5)

        datetime_str = "2000-01-01 10:00"
        sold_date = convert_str_to_tz_aware_datetime(datetime_str)
        self.assertTrue(
            Sale.objects.filter(
                fruit_name="レモン", quantity=1, proceeds=100, sold_on=sold_date
            ).exists()
        )

        datetime_str = "2000-01-01 10:01"
        sold_date = convert_str_to_tz_aware_datetime(datetime_str)
        self.assertTrue(
            Sale.objects.filter(
                fruit_name="ブルーベリー",
                quantity=2,
                proceeds=200,
                sold_on=sold_date,
            ).exists()
        )

        datetime_str = "2000-01-01 10:02"
        sold_date = convert_str_to_tz_aware_datetime(datetime_str)
        self.assertTrue(
            Sale.objects.filter(
                fruit_name="グレープフルーツ",
                quantity=3,
                proceeds=300,
                sold_on=sold_date,
            ).exists()
        )

        datetime_str = "2000-01-01 10:03"
        sold_date = convert_str_to_tz_aware_datetime(datetime_str)
        self.assertTrue(
            Sale.objects.filter(
                fruit_name="パイナップル",
                quantity=4,
                proceeds=400,
                sold_on=sold_date,
            ).exists()
        )

        datetime_str = "2000-01-01 10:04"
        sold_date = convert_str_to_tz_aware_datetime(datetime_str)
        self.assertTrue(
            Sale.objects.filter(
                fruit_name="リンゴ", quantity=5, proceeds=500, sold_on=sold_date
            ).exists()
        )

    def test_csv_file_is_deleted_after_upload(self):

        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)

        Fruit.objects.create(name="レモン", price=100)
        Fruit.objects.create(name="ブルーベリー", price=100)
        Fruit.objects.create(name="グレープフルーツ", price=100)
        Fruit.objects.create(name="パイナップル", price=100)
        Fruit.objects.create(name="リンゴ", price=100)

        with open("sales/tests/test_sales.csv", "r") as csv_file:
            self.client.post(reverse("sale_upload"), {"file_name": csv_file})

        self.assertEqual(CsvUploadFile.objects.count(), 0)
        self.assertFalse(os.listdir("media/csv_files"))

    def test_sale_upload_get_request(self):
        user = CustomUser.objects.create_user("testuser", "123456")
        self.client.force_login(user=user)
        response = self.client.get(reverse("sale_upload"))
        self.assertTemplateUsed(response, "sales/sale_upload.html")
        self.assertIn("form", response.context)
        self.assertIsInstance(response.context["form"], CsvUploadForm)
