from django.urls import include, path
from rest_framework.routers import SimpleRouter

from .views import UserViewSet, get_token, send_confirmation_code

router_v1 = SimpleRouter()
router_v1.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', send_confirmation_code),
    path('v1/auth/token/', get_token)
]
