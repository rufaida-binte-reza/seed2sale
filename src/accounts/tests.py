from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status


class AuthIntegrationTests(APITestCase):
	"""Integration tests for auth endpoints:
	- /api/token/ (djangorestframework-simplejwt)
	- /api/accounts/token/ (custom email-or-phone token view)
	- /api/auth/me/ (current user view)
	"""

	def setUp(self):
		User = get_user_model()
		self.password = 'testpass123'
		self.user = User.objects.create_user(
			email='testuser@example.com',
			phone_number='0123456789',
			password=self.password,
			full_name='Test User',
		)

	def test_global_jwt_token_and_auth_me(self):
		# Obtain token using the global `/api/token/` endpoint
		resp = self.client.post(
			'/api/token/',
			{'email': self.user.email, 'password': self.password},
			format='json'
		)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertIn('access', resp.data)
		token = resp.data['access']

		# Use access token to call /api/auth/me/
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
		me = self.client.get('/api/auth/me/')
		self.assertEqual(me.status_code, status.HTTP_200_OK)
		# Ensure returned user is the created user
		self.assertEqual(me.data.get('id'), self.user.id)

	def test_accounts_custom_token_identifier_and_auth_me(self):
		# Obtain token using the custom accounts token endpoint using phone identifier
		resp = self.client.post(
			'/api/accounts/token/',
			{'identifier': self.user.phone_number, 'password': self.password},
			format='json'
		)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		self.assertIn('access', resp.data)
		token = resp.data['access']

		# Use token to call /api/auth/me/
		self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
		me = self.client.get('/api/auth/me/')
		self.assertEqual(me.status_code, status.HTTP_200_OK)
		self.assertEqual(me.data.get('id'), self.user.id)

