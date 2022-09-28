from .main_router import urlpatterns as main
from .yasg_router import urlpatterns as yasg

from django.conf import settings


urlpatterns = main + yasg

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)