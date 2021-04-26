from django.urls import reverse
from django.test import TestCase

from .models import Fruit
from .forms import StockForm
from users.models import CustomUser

from freezegun import freeze_time


class ModelTests(TestCase):
    @classmethod
    @freeze_time("2021-04-01")
    def setUpTestData(cls):
        Fruit.objects.create(name="apple", price=100)

    # フィールドラベルが正しく表示されるかどうかのテスト

    def test_name_label(self):
        fruit = Fruit.objects.get(id=1)
        field_label = fruit._meta.get_field("name").verbose_name
        self.assertEqual(field_label, "name")

    def test_price_label(self):
        fruit = Fruit.objects.get(id=1)
        field_label = fruit._meta.get_field("price").verbose_name
        self.assertEqual(field_label, "price")

    def test_creation_date_label(self):
        fruit = Fruit.objects.get(id=1)
        field_label = fruit._meta.get_field("created_on").verbose_name
        self.assertEqual(field_label, "created on")

    def test_update_date_label(self):
        fruit = Fruit.objects.get(id=1)
        field_label = fruit._meta.get_field("updated_on").verbose_name
        self.assertEqual(field_label, "updated on")

    # オブジェクトが正しく作成されるかどうかのテスト

    def test_object_name_when_created(self):
        fruit = Fruit.objects.get(id=1)
        self.assertEqual(fruit.name, "apple")
        self.assertNotEqual(fruit.name, "")

    def test_object_price_when_created(self):
        fruit = Fruit.objects.get(id=1)
        self.assertEqual(fruit.price, 100)
        self.assertNotEqual(fruit.price, 0)

    def test_object_creation_datetime_when_created(self):
        fruit = Fruit.objects.get(id=1)
        self.assertEqual("2021-04-01 00:00:00+00:00", str(fruit.created_on))
        self.assertNotEqual("", str(fruit.created_on))

    def test_object_update_datetime_when_created(self):
        fruit = Fruit.objects.get(id=1)
        self.assertEqual("2021-04-01 00:00:00+00:00", str(fruit.updated_on))
        self.assertNotEqual("", str(fruit.updated_on))

    # フィールドのプロパティのテスト

    def test_name_max_length(self):
        fruit = Fruit.objects.get(id=1)
        max_length = fruit._meta.get_field("name").max_length
        self.assertEqual(max_length, 100)

    def test_name_unique(self):
        fruit = Fruit.objects.get(id=1)
        unique = fruit._meta.get_field("name").unique
        self.assertEqual(unique, True)

    def test_price_default_value(self):
        fruit = Fruit.objects.create(name="orange")
        self.assertEqual(fruit.price, 0)

    # オブジェクトが正しく更新されるかどうかのテスト

    def test_object_price_when_updated(self):
        fruit = Fruit.objects.get(id=1)
        fruit.price = 200
        fruit.save()
        self.assertEqual(200, fruit.price)
        self.assertNotEqual(100, fruit.price)

    @freeze_time("2021-04-02")
    def test_object_update_datetime_when_updated(self):
        fruit = Fruit.objects.get(id=1)
        fruit.price = 300
        fruit.save()
        self.assertEqual("2021-04-02 00:00:00+00:00", str(fruit.updated_on))
        self.assertNotEqual("2021-04-01 00:00:00+00:00", str(fruit.updated_on))

    # クラスメソッドのテスト

    def test_str_representation(self):
        fruit = Fruit.objects.get(id=1)
        self.assertEqual("apple", str(fruit))
