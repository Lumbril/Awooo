from django.urls import re_path

from api.views import EmailActivation
from .main_router import urlpatterns as main
from .yasg_router import urlpatterns as yasg

from django.conf import settings


base64_pattern = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'
url_additional = [
    re_path(r'activate/(?P<token>{})'.format(base64_pattern), EmailActivation.as_view())
]

urlpatterns = main + yasg + url_additional

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)