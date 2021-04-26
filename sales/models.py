from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    FileExtensionValidator,
)

from stock.models import Fruit


def reject_future_date_time(value):
    """
    下記のSaleモデルの「sold_on」フィールドの検証方法として使用されます。
    """
    now = timezone.now()
    if value > now:
        raise ValidationError("Future dates are not accepted.")


class Sale(models.Model):

    # 「related_name=sales」を使用すると、テンプレートに以下の記述が可能になります。
    #  {% for sale in fruit.sales.all %}
    fruit = models.ForeignKey(
        Fruit,
        related_name="sales",
        on_delete=models.SET_NULL,  # 親のFruitオブジェクトが削除されても、このSaleオブジェクトは削除されません。
        null=True,
    )

    # 親のFruitオブジェクトが削除された場合に、フルーツの名称を保持するために使用されます。
    fruit_name = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(999999999999)],
    )

    # このSaleオブジェクトが作成されたときの、親のFruitオブジェクトの単価です。
    fruit_price_when_sold = models.PositiveIntegerField(blank=True, null=True)

    # このSaleオブジェクトが作成されたときに受け取ったお金の量（売り上げ）です。
    proceeds = models.PositiveIntegerField(blank=True, null=True)

    # 将来の日時が入力されないようにするカスタムバリデータが含まれている。
    sold_on = models.DateTimeField(validators=[reject_future_date_time])

    class Meta:
        verbose_name = "sale"
        verbose_name_plural = "sales"

    def __str__(self):
        return f"{self.fruit}"

    def save(self, *args, **kwargs):
        # オブジェクトの作成時にのみ実行され、更新時には実行されません。
        if self._state.adding is True:
            self.fruit_name = self.fruit.name
        super(Sale, self).save(*args, **kwargs)

    def retrieve_fruit_price(self):
        self.fruit_price_when_sold = self.fruit.price

    def calculate_proceeds(self):
        self.proceeds = self.fruit_price_when_sold * self.quantity


class CsvUploadFile(models.Model):

    file_name = models.FileField(
        upload_to="csv_files",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "csv",
                ],
                message=[
                    'Please select a file having a ".csv" file extension.'
                ],
            )
        ],
    )

    uploaded_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "CSV file"
        verbose_name_plural = "CSV files"

    def __str__(self):
        return str(self.file_name)

    # アップロードされたCSVファイルをストレージから削除するためにデフォルトのdelete()をオーバーライドする
    def delete(self, *args, **kwargs):
        self.file_name.delete()
        super().delete(*args, **kwargs)
