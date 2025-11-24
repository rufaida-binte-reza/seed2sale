from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer
from rest_framework import viewsets
from .models import FarmerProfile
from .serializers import FarmerProfileSerializer
from .serializers import AddressSerializer
from .models import Address




class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Registration endpoint
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

# Simple profile endpoint
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_view(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
    return Response({"message": "You are authenticated!"})


def login_view(request):
    if request.method == "POST":
        email_or_phone = request.POST.get("email")
        password = request.POST.get("password")

        user = None
        # Try authentication by email or phone
        if '@' in email_or_phone:
            user = authenticate(request, email=email_or_phone, password=password)
        else:
            try:
                u = User.objects.get(phone_number=email_or_phone)
                user = authenticate(request, email=u.email, password=password)
            except User.DoesNotExist:
                pass

        if user is not None:
            login(request, user)
            return redirect("home")  # redirect to homepage
        else:
            messages.error(request, "Invalid credentials")

    return render(request, "app/login.html")


def register_view(request):
    if request.method == "POST":
        full_name = request.POST.get("name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        address = request.POST.get("address")
        password = request.POST.get("password")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
        elif User.objects.filter(phone_number=phone_number).exists():
            messages.error(request, "Phone number already registered.")
        else:
            user = User.objects.create_user(
                email=email,
                phone_number=phone_number,
                full_name=full_name,
                address=address,
                password=password,
            )
            login(request, user)
            return redirect("home")

    return render(request, "app/register.html")


def logout_view(request):
    logout(request)
    return redirect("login")

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()     
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FarmerProfileViewSet(viewsets.ModelViewSet):
    queryset = FarmerProfile.objects.all()
    serializer_class = FarmerProfileSerializer

    def perform_create(self, serializer):
        # Automatically bind logged-in user as farmer
        serializer.save(user=self.request.user)


