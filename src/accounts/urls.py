from django.urls import path
# from . import views

# urlpatterns = [
#     path('login/', views.login_view, name='login'),
#     path('register/', views.register_view, name='register'),
#     path('logout/', views.logout_view, name='logout'),
# ]

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import protected_view 

# urlpatterns = [
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('api/protected/', protected_view, name='protected_view'),

# ]

# from .views import RegisterUserView, user_profile

# urlpatterns = [
#     path('register/', RegisterUserView.as_view(), name='register'),
#     path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
#     path('profile/', user_profile, name='profile'),
# ]

from .auth import EmailOrPhoneTokenObtainView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.routers import DefaultRouter
from .views import FarmerProfileViewSet
from django.urls import path, include
from .views import (
    RegisterView,
    profile_view,
    AddressViewSet,
)

router = DefaultRouter()
router.register(r'farmers', FarmerProfileViewSet, basename='farmers')
router.register('addresses', AddressViewSet, basename='address')


urlpatterns = router.urls

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', EmailOrPhoneTokenObtainView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile/', profile_view, name='profile'),
    path('register/', RegisterView.as_view(), name="register"),
]
