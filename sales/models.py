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
    Validation method for the "sold_on" field of the Sale model.
    """
    now = timezone.now()
    if value > now:
        raise ValidationError("Future dates are not accepted.")


class Sale(models.Model):

    # on_delete=models.SET_NULL is used to ensure that this Sale object is not
    # deleted if the parent Fruit object is deleted.
    fruit = models.ForeignKey(
        Fruit,
        related_name="sales",
        on_delete=models.SET_NULL,
        null=True,
    )

    # Used to retain the name of the parent fruit even if the fruit is deleted.
    fruit_name = models.CharField(max_length=100)

    quantity = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(999999999999)],
    )

    # The price of the parent Fruit object when this Sale object is created.
    fruit_price_when_sold = models.PositiveIntegerField(blank=True, null=True)

    # The amount of money received when this Sale object is created.
    proceeds = models.PositiveIntegerField(blank=True, null=True)

    # Includes a custom validator to ensure that future dates are not entered.
    sold_on = models.DateTimeField(validators=[reject_future_date_time])

    class Meta:
        verbose_name = "sale"
        verbose_name_plural = "sales"

    def __str__(self):
        return f"{self.fruit}"

    def save(self, *args, **kwargs):
        # Only executed when the Sale object is created, not when updated.
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

    # The default delete function is overidden to ensure that the associated
    # user-uploaded csv file is deleted as well as the object.
    def delete(self, *args, **kwargs):
        self.file_name.delete()
        super().delete(*args, **kwargs)
