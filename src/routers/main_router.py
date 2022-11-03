import os

from django.conf.urls.static import static
from django.urls import include, path

from django.contrib import admin

from Awooo import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('routers.api_router')),
]

if os.getenv("LEVEL") != "PROD":
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
