from django.test import TestCase

from sales.forms import CsvUploadForm


class CsvUploadFormTests(TestCase):
    def test_csv_upload_form_required_fields(self):
        form = CsvUploadForm()
        self.assertTrue(form.fields["file_name"].required)

    def test_csv_form_field_error_messages(self):
        error_messages = {
            "empty": "The selected file is empty.",
            "required": "Please select a CSV file.",
            "missing": "A file has not been provided.",
            "invalid": "The file format is not correct. Please select a CSV file.",
            "contradiction": "Please either submit a file or check the clear checkbox, not both.",
            "max_length": "",
        }
        form = CsvUploadForm()
        self.assertEqual(
            form.fields["file_name"].error_messages, error_messages
        )

    def test_csv_form_field_labels(self):
        form = CsvUploadForm()
        self.assertEqual(form.fields["file_name"].label, "Filename")

    def test_csv_form_when_valid(self):
        with open("sales/tests/test_sales.csv", "r") as csv_file:
            form = CsvUploadForm({"file_name": csv_file})
            self.assertTrue(form.is_multipart)
            self.assertTrue(form.is_bound)
            self.assertTrue(form.is_valid)
