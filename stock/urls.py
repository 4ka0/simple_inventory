from django.urls import path

from .views import stock_list, stock_create, stock_update, stock_delete


urlpatterns = [
    path("list/", stock_list, name="stock_list"),
    path("create/", stock_create, name="stock_create"),
    path("<int:pk>/update/", stock_update, name="stock_update"),
    path("<int:pk>/delete/", stock_delete, name="stock_delete"),
]
