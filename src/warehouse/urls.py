from rest_framework.routers import DefaultRouter
from .views import WarehouseViewSet, InventoryViewSet

router = DefaultRouter()
router.register('warehouses', WarehouseViewSet)
router.register('inventory', InventoryViewSet)

urlpatterns = router.urls
