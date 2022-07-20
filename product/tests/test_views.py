import os
import shutil

from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase, override_settings
from rest_framework import status

from category.models import Category
from base_services import generate_image, get_access_token


@override_settings(MEDIA_ROOT=os.path.join(os.path.join(settings.BASE_DIR, 'media_test')))
class ProductTestCase(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='user_1', password='pass1234')
		self.access_token_for_user = get_access_token(self.user)
		self.superuser = User.objects.create_superuser(username='user_2', password='pass1234')
		self.access_token_for_superuser = get_access_token(self.superuser)
		self.category = Category.objects.create(title='Category 1')

		self.data = {
			'title':'Product 1',
			'description': 'de21scription for product 1',
			'price': '123.00',
			'category': self.category.id,
			'image': generate_image(),
		}

		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_superuser)
		self.product = self.client.post(reverse('products'), self.data)

	def tearDown(self):
		path = settings.MEDIA_ROOT
		shutil.rmtree(path)

	def test_product_get_by_title_not_found(self):
		response = self.client.get(reverse('products'), {'title': 'title'})
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_product_get_by_title(self):
		title = self.product.data.get('title')
		response = self.client.get(reverse('products'), {'title': title})
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_product_list(self):
		response = self.client.get(reverse('products'))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_product_create_unauth(self):
		self.client.credentials(HTTP_AUTHORIZATION='')
		response = self.client.post(reverse('products'), self.data)
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_product_create_forbidden(self):
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
		response = self.client.post(reverse('products'), self.data)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_product_create(self):
		self.data['title'] = 'Product 1223'
		self.data['image'] = generate_image()
		response = self.client.post(reverse('products'), self.data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_product_detail_not_found(self):
		response = self.client.get(reverse('detail-product', kwargs={'product_id': 122}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_product_detail(self):
		product_id = self.product.data.get('id')
		response = self.client.get(reverse('detail-product', kwargs={'product_id': product_id}))
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_product_delete_unauth(self):
		product_id = self.product.data.get('id')
		self.client.credentials(HTTP_AUTHORIZATION='')
		response = self.client.delete(reverse('detail-product', kwargs={'product_id': product_id}))
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_product_delete_forbidden(self):
		product_id = self.product.data.get('id')
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
		response = self.client.delete(reverse('detail-product', kwargs={'product_id': product_id}))
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_product_delete_not_found(self):
		response = self.client.delete(reverse('detail-product', kwargs={'product_id': 12121}))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_product_delete(self):
		product_id = self.product.data.get('id')
		response = self.client.delete(reverse('detail-product', kwargs={'product_id': product_id}))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)




