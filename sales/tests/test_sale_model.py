from django.test import TestCase
from django.utils import timezone

from stock.models import Fruit
from sales.models import Sale

from freezegun import freeze_time


class SaleModelTests(TestCase):
    @classmethod
    @freeze_time("2021-04-01")
    def setUpTestData(cls):

        Fruit.objects.create(name="apple", price=100)
        apple = Fruit.objects.get(id=1)

        Sale.objects.create(
            fruit=apple,
            fruit_price_when_sold=100,
            quantity=3,
            proceeds=300,
            sold_on=timezone.now(),
        )

    # フィールドラベルが正しく表示されるかどうかのテスト

    def test_fruit_label(self):
        sale = Sale.objects.get(id=1)
        field_label = sale._meta.get_field("fruit").verbose_name
        self.assertEqual(field_label, "fruit")

    def test_fruit_name_label(self):
        sale = Sale.objects.get(id=1)
        field_label = sale._meta.get_field("fruit_name").verbose_name
        self.assertEqual(field_label, "fruit name")

    def test_quantity_label(self):
        sale = Sale.objects.get(id=1)
        field_label = sale._meta.get_field("quantity").verbose_name
        self.assertEqual(field_label, "quantity")

    def test_fruit_price_when_sold_label(self):
        sale = Sale.objects.get(id=1)
        field_label = sale._meta.get_field(
            "fruit_price_when_sold"
        ).verbose_name
        self.assertEqual(field_label, "fruit price when sold")

    def test_proceeds_label(self):
        sale = Sale.objects.get(id=1)
        field_label = sale._meta.get_field("proceeds").verbose_name
        self.assertEqual(field_label, "proceeds")

    def test_sold_on_label(self):
        sale = Sale.objects.get(id=1)
        field_label = sale._meta.get_field("sold_on").verbose_name
        self.assertEqual(field_label, "sold on")

    # オブジェクトが正しく作成されるかどうかのテスト

    def test_object_fruit_when_created(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(sale.fruit.name, "apple")

    def test_object_fruit_name_when_created(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(sale.fruit_name, "apple")

    def test_object_quantity_when_created(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(sale.quantity, 3)

    def test_object_sold_datetime_when_created(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(str(sale.sold_on), "2021-04-01 00:00:00+00:00")

    def test_object_proceeds_when_created(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(sale.proceeds, 300)

    def test_object_fruit_price_sold_when_created(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(sale.fruit_price_when_sold, 100)

    # 親オブジェクトのデータフィールドにアクセスできるかどうかのテスト

    def test_parent_object_name_field(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(sale.fruit.name, "apple")

    def test_parent_object_price_field(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(sale.fruit.price, 100)

    def test_parent_object_created_on_field(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(
            str(sale.fruit.created_on), "2021-04-01 00:00:00+00:00"
        )

    def test_parent_object_updated_on_field(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual(
            str(sale.fruit.updated_on), "2021-04-01 00:00:00+00:00"
        )

    # フィールドのプロパティのテスト

    def test_fruit_name_max_length(self):
        sale = Sale.objects.get(id=1)
        max_length = sale._meta.get_field("fruit_name").max_length
        self.assertEqual(max_length, 100)

    # オブジェクトが正しく更新されるかどうかのテスト

    def test_quantity_and_proceeds_when_quantity_updated(self):
        sale = Sale.objects.get(id=1)
        sale.quantity = 6
        sale.calculate_proceeds()
        sale.save()
        self.assertEqual(sale.quantity, 6)
        self.assertNotEqual(sale.quantity, 3)
        self.assertEqual(sale.proceeds, 600)
        self.assertNotEqual(sale.proceeds, 300)

    @freeze_time("2021-05-05")
    def test_sold_datetime_when_updated(self):
        sale = Sale.objects.get(id=1)
        sale.sold_on = timezone.now()
        sale.save()
        self.assertEqual("2021-05-05 00:00:00+00:00", str(sale.sold_on))
        self.assertNotEqual("2021-04-01 00:00:00+00:00", str(sale.sold_on))

    # クラスメソッドのテスト

    def test_str_representation(self):
        sale = Sale.objects.get(id=1)
        self.assertEqual("apple", str(sale))

    # 親オブジェクトの削除による影響がないことを確認する

    def test_parent_object_count_after_deletion(self):
        new_fruit = Fruit.objects.create(name="orange", price=200)
        Sale.objects.create(
            fruit=new_fruit, quantity=2, proceeds=400, sold_on=timezone.now()
        )
        self.assertEqual(Fruit.objects.count(), 2)
        self.assertEqual(Sale.objects.count(), 2)
        new_fruit.delete()
        self.assertEqual(Fruit.objects.count(), 1)
        self.assertEqual(Sale.objects.count(), 2)

    @freeze_time("2021-06-06")
    def test_child_object_properties_unaffected_after_deletion(self):
        new_fruit = Fruit.objects.create(name="banana", price=300)
        new_sale = Sale.objects.create(
            fruit=new_fruit,
            quantity=3,
            fruit_price_when_sold=300,
            proceeds=900,
            sold_on=timezone.now(),
        )
        new_fruit.delete()
        self.assertEqual(new_sale.fruit_name, "banana")
        self.assertEqual(new_sale.quantity, 3)
        self.assertEqual(new_sale.fruit_price_when_sold, 300)
        self.assertEqual(new_sale.proceeds, 900)
        self.assertEqual(str(new_sale.sold_on), "2021-06-06 00:00:00+00:00")

    def test_child_object_properties_unaffected_after_parent_updated(self):
        fruit = Fruit.objects.get(id=1)
        sale = Sale.objects.get(id=1)
        # 現在の値を確認する
        self.assertEqual(fruit.price, 100)
        self.assertEqual(sale.fruit_price_when_sold, 100)
        self.assertEqual(sale.proceeds, 300)
        # 果物の単価を更新する
        fruit.price = 200
        # saleのfruit_price_when_soldまたはproceedsが変わっていないか確認する
        self.assertEqual(fruit.price, 200)
        self.assertEqual(sale.fruit_price_when_sold, 100)
        self.assertEqual(sale.proceeds, 300)

    def test_sale_proceeds_updated_based_on_original_fruit_price(self):
        fruit = Fruit.objects.get(id=1)
        sale = Sale.objects.get(id=1)
        # 果物の単価を更新する
        fruit.price = 200
        # saleのquantityをを更新する
        sale.quantity = 6
        sale.calculate_proceeds()
        sale.save()
        # 売上高は、果物の新しい単価ではなく、saleオブジェクトが最初に作成されたときの
        # 単価（100）に基づいて再計算されなければなりません。
        self.assertEqual(fruit.price, 200)
        self.assertEqual(sale.fruit_price_when_sold, 100)
        self.assertEqual(sale.quantity, 6)
        self.assertEqual(sale.proceeds, 600)
