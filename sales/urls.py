from django.urls import path

from .views import (
    sale_list,
    sale_create,
    sale_update,
    sale_delete,
    sale_upload,
)


urlpatterns = [
    path("list/", sale_list, name="sale_list"),
    path("create/", sale_create, name="sale_create"),
    path("<int:pk>/update/", sale_update, name="sale_update"),
    path("<int:pk>/delete/", sale_delete, name="sale_delete"),
    path("upload/", sale_upload, name="sale_upload"),
]
