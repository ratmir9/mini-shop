from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from base_services import get_access_token


class RegisterTestCase(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user_2', password='password1234')
		self.data = {
			'username': 'example_1',
			'email': 'example@gmail.com',
			'password': 'password1234',
			'password2': 'password1234'
		}

	def test_register_bad_request(self):
		self.data['password'] = 'password123'
		response = self.client.post(reverse('register'), self.data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

	def test_register(self):
		response = self.client.post(reverse('register'), self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_register_user_exists(self):
		self.data['username'] = 'user_2'
		response = self.client.post(reverse('register'), self.data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTestCase(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='ratmir', password='password1234')
		self.data = {
			'username': self.user.username,
			'password': 'password1234'
		}

	def test_login_un_auth(self):
		data = {
			'username': 'ratmir',
			'password': 'password123'
		}
		response = self.client.post(reverse('token_obtain_pair'), data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_login(self):
		response = self.client.post(reverse('token_obtain_pair'), self.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	

class UserTestCase(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user_1', password='pass1234')
		self.access_token_for_user = get_access_token(self.user)
		self.superuser = User.objects.create_superuser(username='super_user', password='pass1234')
		self.access_token_for_superuser = get_access_token(self.superuser)
		self.user_2 = User.objects.create_user(username='user_2', password='pass1234')
		self.access_token_for_user_2 = get_access_token(self.user_2)

	def test_user_list_un_auth(self):
		response = self.client.get(reverse('users'))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_user_list_forbidden(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
		response = self.client.get(reverse('users'))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_user_list(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_superuser)
		response = self.client.get(reverse('users'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_user_detail_not_found(self):
		response = self.client.get(reverse('detail-user', kwargs={'user_id': 1234}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)		

	def test_user_detail(self):
		user_id = self.user.id
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_superuser)
		response = self.client.get(reverse('detail-user', kwargs={'user_id': user_id}))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_user_delete_un_auth(self):
		user_id = self.user.id
		response = self.client.delete(reverse('detail-user', kwargs={'user_id': user_id}))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_user_delete_forbidden(self):
		user_id = self.user.id
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user_2)
		response = self.client.delete(reverse('detail-user', kwargs={'user_id': user_id}))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_user_delete_not_found(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
		response = self.client.delete(reverse('detail-user', kwargs={'user_id': 1234}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_user_delete(self):
		user_id = self.user.id
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
		response = self.client.delete(reverse('detail-user', kwargs={'user_id': user_id}))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		