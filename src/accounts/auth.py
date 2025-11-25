# accounts/auth.py
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

class EmailOrPhoneTokenObtainSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # keep compatibility with parent
    identifier = serializers.CharField(required=False, write_only=True)

    def __init__(self, *args, **kwargs):
        # Make the parent `username_field` optional so clients can use `identifier` instead
        super().__init__(*args, **kwargs)
        if self.username_field in self.fields:
            self.fields[self.username_field].required = False

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
                    UserModel = get_user_model()
                    user = UserModel.objects.filter(email__iexact=identifier).first()
                    if not user:
                        user = UserModel.objects.filter(phone_number__iexact=identifier).first()
                except Exception as e:
                    print('User lookup exception:', e)
                    user = None
                # debug logging removed
                if user and user.check_password(password):
                    self.user = user
                    # ensure parent serializer sees a 'username_field' in attrs
                    # (TokenObtainPairSerializer expects the username field to be present)
                    attrs[self.username_field] = user.email or user.phone_number
                else:
                    raise serializers.ValidationError('No active account found with given credentials')
            else:
                # fallback to default flow (username field)
                self.user = authenticate(request=request, username=attrs.get('username'), password=password)
        else:
            self.user = None

        if not getattr(self, 'user', None):
            # fallback: try authenticate with email or phone via backend
            UserModel = get_user_model()
            user = UserModel.objects.filter(email__iexact=attrs.get('email')).first() or \
                   UserModel.objects.filter(phone_number__iexact=attrs.get('email')).first()
            if user and user.check_password(password):
                self.user = user
                # ensure parent sees the username_field (email) value
                attrs[self.username_field] = user.email or user.phone_number

        if not self.user:
            raise serializers.ValidationError("Invalid credentials")

        return super().validate(attrs)


class EmailOrPhoneTokenObtainView(TokenObtainPairView):
    serializer_class = EmailOrPhoneTokenObtainSerializer
