from rest_framework import viewsets, permissions
from .models import DriverProfile, DeliveryJob
from .serializers import DriverProfileSerializer, DeliveryJobSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class DriverProfileViewSet(viewsets.ModelViewSet):
    queryset = DriverProfile.objects.select_related('user').all()
    serializer_class = DriverProfileSerializer
    permission_classes = [permissions.IsAdminUser]

class DeliveryJobViewSet(viewsets.ModelViewSet):
    queryset = DeliveryJob.objects.select_related('order','driver').all()
    serializer_class = DeliveryJobSerializer
    permission_classes = [permissions.IsAuthenticated]
