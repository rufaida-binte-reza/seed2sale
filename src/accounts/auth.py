# accounts/auth.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework import serializers

class EmailOrPhoneTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # not actually used

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['phone_number'] = user.phone_number
        token['full_name'] = user.full_name
        return token

    def validate(self, attrs):
        # Accept either email or phone_number + password
        username = attrs.get('username') or attrs.get('email') or attrs.get('identifier')
        password = attrs.get('password')
        # If identifier in request data, try to resolve user
        request = self.context.get('request')
        if request:
            identifier = request.data.get('identifier')  # prefer identifier
            if identifier:
                # Try email then phone
                try:
                    user = User.objects.filter(email__iexact=identifier).first()
                    if not user:
                        user = User.objects.filter(phone_number__iexact=identifier).first()
                except:
                    user = None
                if user and user.check_password(password):
                    self.user = user
                else:
                    raise serializers.ValidationError('No active account found with given credentials')
            else:
                # fallback to default flow (username field)
                self.user = authenticate(request=request, username=attrs.get('username'), password=password)
        else:
            self.user = None

        if not getattr(self, 'user', None):
            # fallback: try authenticate with email or phone via backend
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()
            user = UserModel.objects.filter(email__iexact=attrs.get('email')).first() or \
                   UserModel.objects.filter(phone_number__iexact=attrs.get('email')).first()
            if user and user.check_password(password):
                self.user = user

        if not self.user:
            raise serializers.ValidationError("Invalid credentials")

        return super().validate(attrs)


class EmailOrPhoneTokenObtainView(TokenObtainPairView):
    serializer_class = EmailOrPhoneTokenObtainSerializer
