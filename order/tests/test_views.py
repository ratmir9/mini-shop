import os
import shutil

from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase, override_settings

from category.models import Category
from base_services import get_access_token, generate_image
from basket.serializers import BasketCreateSerializer

@override_settings(MEDIA_ROOT=os.path.join(settings.BASE_DIR, 'media_test'))
class OrderTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_1', password='1234pass')
        self.access_token_for_user = get_access_token(self.user)
        self.superuser = User.objects.create_superuser(username='superuser_1', password='1234pass')
        self.access_token_for_superuser = get_access_token(self.superuser)
        self.category = Category.objects.create(title='Category 1')
        self.data_for_product_1 = {
            'title': 'Product 1',
            'description': 'description for product 1',
            'price': 123.00,
            'category': self.category.id,
            'image': generate_image()
        }
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_superuser) 
        self.product_1 = self.client.post(reverse('products'), self.data_for_product_1)

        self.data_for_order = {
            'products': [
                {
                    'product_id': self.product_1.data.get('id')
                }
            ],
            'username': 'user test',
            'phone': '12354'
        }

        self.order_1 = self.client.post(reverse('orders'), self.data_for_order, format='json')
    
    def tearDown(self):
        path = settings.MEDIA_ROOT
        shutil.rmtree(path)

    def test_order_list_un_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_list_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_list(self):
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_create_un_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(reverse('orders'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
           
    def test_order_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.post(reverse('orders'), self.data_for_order, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_order_detail_un_auth(self):
        order_id = self.order_1.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(reverse('detail-order', kwargs={'order_id':order_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_detail_forbidden(self):
        order_id = self.order_1.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.get(reverse('detail-order', kwargs={'order_id':order_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_detail_not_found(self):
        response = self.client.get(reverse('detail-order', kwargs={'order_id': 123}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_detail(self):
        order_id = self.order_1.data.get('id')
        response = self.client.get(reverse('detail-order', kwargs={'order_id':order_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_order_delete_un_auth(self):
        order_id = self.order_1.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.delete(reverse('detail-order', kwargs={'order_id':order_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_order_delete_forbidden(self):
        order_id = self.order_1.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.delete(reverse('detail-order', kwargs={'order_id':order_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_order_delete_not_found(self):
        response = self.client.delete(reverse('detail-order', kwargs={'order_id': 123}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_order_delete(self):
        order_id = self.order_1.data.get('id')
        response = self.client.delete(reverse('detail-order', kwargs={'order_id':order_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)