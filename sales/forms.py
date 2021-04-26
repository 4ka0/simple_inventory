from django import forms

from .models import Sale
from .models import CsvUploadFile
from stock.models import Fruit


class SaleCreateForm(forms.ModelForm):

    fruit = forms.ModelChoiceField(
        label="Fruit",
        error_messages={
            "required": "Please select one item from the dropdown list.",
            "invalid_choice": "Please select a valid item.",
        },
        queryset=Fruit.objects.all(),
    )

    quantity = forms.CharField(
        label="Quantity",
        error_messages={
            "required": "Required.",
            "invalid": "Please use digits.",
            "max_value": "Please enter a number between 0 and 999999999999.",
            "min_value": "Please enter a number between 0 and 999999999999.",
        },
    )

    sold_on = forms.DateTimeField(
        label="Sale date and time",
        error_messages={
            "required": "Required.",
            "invalid": "Please enter a valid date and time.",
        },
        help_text='Please use the format "YYYY-MM-DD HH:MM" (e.g. 2021-04-01 09:00).',
        input_formats=["%Y-%m-%d %H:%i"],
    )

    class Meta:

        model = Sale

        fields = (
            "fruit",
            "quantity",
            "sold_on",
        )


class SaleUpdateForm(forms.ModelForm):

    quantity = forms.CharField(
        label="Quantity",
        error_messages={
            "required": "Required.",
            "invalid": "Please use digits.",
            "max_value": "Please enter a number between 0 and 999999999999.",
            "min_value": "Please enter a number between 0 and 999999999999.",
        },
    )

    sold_on = forms.DateTimeField(
        label="Sale date and time",
        error_messages={
            "required": "Required.",
            "invalid": "Please enter a valid date and time.",
        },
        help_text='Please use the format "YYYY-MM-DD HH:MM" (e.g. 2021-04-01 09:00).',
        input_formats=["%Y-%m-%d %H:%i"],
        widget=forms.DateTimeInput(format="%Y-%m-%d %H:%M"),
    )

    class Meta:

        model = Sale

        fields = (
            "quantity",
            "sold_on",
        )


class CsvUploadForm(forms.ModelForm):

    file_name = forms.FileField(
        label="Filename",
        error_messages={
            "empty": "The selected file is empty.",
            "required": "Please select a CSV file.",
            "missing": "A file has not been provided.",
            "invalid": "The file format is not correct. Please select a CSV file.",
        },
    )

    class Meta:

        model = CsvUploadFile

        fields = ("file_name",)
