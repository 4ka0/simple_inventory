from django.contrib import admin
from .models import Fruit


class FruitAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "created_on", "updated_on")


admin.site.register(Fruit, FruitAdmin)
