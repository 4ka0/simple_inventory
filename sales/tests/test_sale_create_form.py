from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from stock.models import Fruit
from sales.forms import SaleCreateForm

from freezegun import freeze_time


class SaleCreateFormTests(TestCase):
    def test_create_sale_form_required_fields(self):
        form = SaleCreateForm()
        self.assertTrue(form.fields["fruit"].required)
        self.assertTrue(form.fields["quantity"].required)

    def test_create_sale_form_field_error_messages(self):
        fruit_error_messages = {
            "required": "Please select one item from the dropdown list.",
            "invalid_choice": "Please select a valid item.",
        }
        quantity_error_messages = {
            "required": "Required.",
            "invalid": "Please use digits.",
            "max_value": "Please enter a number between 0 and 999999999999.",
            "min_value": "Please enter a number between 0 and 999999999999.",
        }
        form = SaleCreateForm()
        self.assertEqual(
            form.fields["fruit"].error_messages, fruit_error_messages
        )
        self.assertEqual(
            form.fields["quantity"].error_messages, quantity_error_messages
        )

    @freeze_time("2021-06-01")
    def test_create_sale_form_when_valid(self):

        apple = Fruit.objects.create(name="apple", price=100)

        form = SaleCreateForm(
            {"fruit": apple.id, "quantity": 3, "sold_on": timezone.now()}
        )

        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertEqual(form.errors.as_text(), "")

        self.assertEqual(form.cleaned_data["fruit"], apple)
        self.assertEqual(form.cleaned_data["quantity"], "3")
        self.assertEqual(
            str(form.cleaned_data["sold_on"]), "2021-06-01 00:00:00+00:00"
        )

        # boundデータを確認
        form_output = []

        for boundfield in form:
            form_output.append([boundfield.label, boundfield.data])

        expected_output = [
            ["Fruit", apple.id],
            ["Quantity", 3],
            ["Sale date and time", timezone.now()],
        ]

        self.assertEqual(form_output, expected_output)

    def test_create_sale_form_when_empty(self):
        form = SaleCreateForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())
        with self.assertRaises(AttributeError):
            form.cleaned_data

    def test_create_sale_form_when_partially_empty(self):
        apple = Fruit.objects.create(name="apple", price=100)
        form = SaleCreateForm({"fruit": apple.id})
        self.assertEqual(form.errors["quantity"], ["Required."])
        self.assertFalse(form.is_valid())

    def test_future_date_fails(self):
        apple = Fruit.objects.create(name="apple", price=100)
        form = SaleCreateForm(
            {
                "fruit": apple.id,
                "quantity": 3,
                "sold_on": timezone.now() + timedelta(days=1),
            }
        )
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors, {"sold_on": ["Future dates are not accepted."]}
        )
