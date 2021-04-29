from django.test import TestCase

from ..forms import StockForm


class StockFormTests(TestCase):
    def test_create_stock_form_required_fields(self):
        form = StockForm()
        self.assertTrue(form.fields["name"].required)
        self.assertTrue(form.fields["price"].required)

    def test_create_stock_form_field_error_messages(self):
        name_error_messages = {
            "required": "Required.",
            "unique": "This name has already been registered.",
            "max_length": "Please use less than 100 characters.",
        }
        price_error_messages = {
            "required": "Required.",
            "invalid": "Please use digits.",
            "max_value": "Please enter a number between 0 and 999999999999.",
            "min_value": "Please enter a number between 0 and 999999999999.",
        }
        form = StockForm()
        self.assertEqual(
            form.fields["name"].error_messages, name_error_messages
        )
        self.assertEqual(
            form.fields["price"].error_messages, price_error_messages
        )

    def test_create_stock_form_when_valid(self):
        form = StockForm(
            {
                "name": "lemon",
                "price": 200,
            }
        )

        self.assertTrue(form.is_bound)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.errors, {})
        self.assertEqual(form.errors.as_text(), "")

        self.assertEqual(form.cleaned_data["name"], "lemon")
        self.assertEqual(form.cleaned_data["price"], "200")

        # boundデータを確認
        form_output = []

        for boundfield in form:
            form_output.append([boundfield.label, boundfield.data])

        expected_output = [
            ["Name", "lemon"],
            ["Price", 200],
        ]

        self.assertEqual(form_output, expected_output)

    def test_create_stock_form_when_empty(self):
        form = StockForm()
        self.assertFalse(form.is_bound)
        self.assertFalse(form.is_valid())
        with self.assertRaises(AttributeError):
            form.cleaned_data

    def test_create_stock_form_when_partially_empty(self):
        form = StockForm({"name": "orange"})
        self.assertEqual(form.errors["price"], ["Required."])
        self.assertFalse(form.is_valid())
