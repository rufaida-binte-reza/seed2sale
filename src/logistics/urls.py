from rest_framework.routers import DefaultRouter
from .views import DriverProfileViewSet, DeliveryJobViewSet

router = DefaultRouter()
router.register('drivers', DriverProfileViewSet)
router.register('jobs', DeliveryJobViewSet)

urlpatterns = router.urls
