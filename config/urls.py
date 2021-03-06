from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("fish1234/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("home.urls")),
    path("stock/", include("stock.urls")),
    path("sales/", include("sales.urls")),
    path("stats/", include("stats.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
