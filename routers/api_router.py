from rest_framework.routers import DefaultRouter
from rest_framework.urls import path

from api import views as views_api


router = DefaultRouter(trailing_slash=False)

urlpatterns = router.urls
