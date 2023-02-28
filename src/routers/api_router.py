from rest_framework.routers import DefaultRouter
from rest_framework.urls import path

from api import views as views_api


router = DefaultRouter(trailing_slash=False)
router.register('account', views_api.RecoveryView, basename='recovery')
router.register('account', views_api.UserView, basename='about me')
router.register('account', views_api.AccountView, basename='registration')
router.register('dogs', views_api.DogView, basename='dogs')
router.register('subscriber', views_api.SubscriberView, basename='subscriber')
router.register('subscription', views_api.SubscriptionView, basename='subscription')
router.register('file', views_api.UploadFileView, basename='file upload')

additional_urlpatterns = [
    path('account/authenticate', views_api.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('account/reissueJwt', views_api.CustomTokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = router.urls
urlpatterns += additional_urlpatterns
