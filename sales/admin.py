from django.contrib import admin
from .models import Sale
from .models import CsvUploadFile


class SaleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "fruit",
        "fruit_name",
        "quantity",
        "proceeds",
        "sold_on",
    )


admin.site.register(Sale, SaleAdmin)
admin.site.register(CsvUploadFile)
