from django.test import TestCase
from django.utils import timezone

from sales.models import CsvUploadFile

from freezegun import freeze_time


class CsvUploadFileModelTests(TestCase):
    @classmethod
    @freeze_time("2020-01-01")
    def setUpTestData(cls):
        CsvUploadFile.objects.create(
            file_name="sales/tests/test_sales.csv", uploaded_on=timezone.now()
        )

    def test_file_name_label(self):
        csvfile = CsvUploadFile.objects.get(id=1)
        field_label = csvfile._meta.get_field("file_name").verbose_name
        self.assertEqual(field_label, "file name")

    def test_uploaded_on_label(self):
        csvfile = CsvUploadFile.objects.get(id=1)
        field_label = csvfile._meta.get_field("uploaded_on").verbose_name
        self.assertEqual(field_label, "uploaded on")

    def test_object_file_name_when_created(self):
        csvfile = CsvUploadFile.objects.get(id=1)
        self.assertEqual(csvfile.file_name, "sales/tests/test_sales.csv")

    @freeze_time("2020-01-01")
    def test_object_uploaded_date_when_created(self):
        csvfile = CsvUploadFile.objects.get(id=1)
        self.assertEqual(csvfile.uploaded_on, timezone.now())

    def test_str_representation(self):
        csvfile = CsvUploadFile.objects.get(id=1)
        self.assertEqual("sales/tests/test_sales.csv", str(csvfile))
