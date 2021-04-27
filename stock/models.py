from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Fruit(models.Model):

    # unique=True ensures that fruits having identical names can't be created
    name = models.CharField(max_length=100, unique=True)

    price = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(999999999999)],
    )

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "fruit"
        verbose_name_plural = "fruits"

    def __str__(self):
        return f"{self.name}"
