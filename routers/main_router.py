from django.urls import include, path

from django.contrib import admin


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('routers.api_router')),
]
