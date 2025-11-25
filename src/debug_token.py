import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'seed2sale.settings')
import django
django.setup()

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
user, created = User.objects.get_or_create(
    email='testuser@example.com',
    defaults={'phone_number':'0123456789','full_name':'Test User'}
)
if created:
    user.set_password('testpass123')
    user.save()
client = APIClient()
resp = client.post('/api/accounts/token/', {'identifier':'0123456789','password':'testpass123'}, format='json')
print('status:', resp.status_code)
try:
    print('data:', resp.data)
except Exception as e:
    print('resp content:', resp.content)

# Debug serializer behavior
from accounts.auth import EmailOrPhoneTokenObtainSerializer
ser = EmailOrPhoneTokenObtainSerializer(data={'identifier':'0123456789','password':'testpass123'}, context={'request': None})
print('email field required:', ser.fields.get('email').required if 'email' in ser.fields else None)
print('identifier field required:', ser.fields.get('identifier').required if 'identifier' in ser.fields else None)
print('ser.is_valid():', ser.is_valid())
print('ser.errors:', ser.errors)

resp2 = client.post('/api/accounts/token/', {'email':'testuser@example.com','password':'testpass123'}, format='json')
print('\nPOST with email:', resp2.status_code)
print('data:', getattr(resp2, 'data', resp2.content))

UserModel = get_user_model()
user_by_phone = UserModel.objects.filter(phone_number__iexact='0123456789').first()
print('\nUser by phone:', user_by_phone)
if user_by_phone:
    print('check_password:', user_by_phone.check_password('testpass123'))
