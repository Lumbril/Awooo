from rest_framework.routers import DefaultRouter
from rest_framework.urls import path

from api import views as views_api


router = DefaultRouter(trailing_slash=False)
router.register('account', views_api.RecoveryView, basename='recovery')

additional_urlpatterns = [
    path('account/registration', views_api.AccountView.as_view(), name='registration'),
    path('account/authenticate', views_api.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/reissueJwt', views_api.CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('account/me', views_api.UserView.as_view(), name='about me')
]

urlpatterns = router.urls
urlpatterns += additional_urlpatterns
