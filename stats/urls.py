from django.urls import path

from .views import stats_list


urlpatterns = [
    path("list/", stats_list, name="stats_list"),
]
