from django import forms

from .models import Fruit


class StockForm(forms.ModelForm):

    name = forms.CharField(
        label="Name",
        error_messages={
            "required": "Required.",
            "unique": "This name has already been registered.",
            "max_length": "Please use less than 100 characters.",
        },
    )

    price = forms.CharField(
        label="Price",
        error_messages={
            "required": "Required.",
            "invalid": "Please use digits.",
            "max_value": "Please enter a number between 0 and 999999999999.",
            "min_value": "Please enter a number between 0 and 999999999999.",
        },
    )

    class Meta:

        model = Fruit

        fields = (
            "name",
            "price",
        )
