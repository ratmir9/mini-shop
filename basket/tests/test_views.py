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
class BasketTestCase(APITestCase):
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

        self.data_for_basket = {
            'products': [
                {
                    'product_id': self.product_1.data.get('id')
                }
            ]
        }

        self.basket_1 = self.client.post(reverse('baskets'), self.data_for_basket, format='json')

    def tearDown(self):
        path = settings.MEDIA_ROOT
        shutil.rmtree(path)

    def test_basket_list_un_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(reverse('baskets'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_basket_list_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.get(reverse('baskets'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_basket_list(self):
        response = self.client.get(reverse('baskets'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_basket_create_un_auth(self):
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.post(reverse('baskets'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
    def test_basket_create_bad_request(self):
        self.data_for_basket['products'] = []
        serializer = BasketCreateSerializer(data=self.data_for_basket)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        serializer.is_valid() 
        response = self.client.post(reverse('baskets'), self.data_for_basket, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, serializer.errors)
       
    def test_basket_create(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.post(reverse('baskets'), self.data_for_basket, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_basket_detail_un_auth(self):
        basket_id = self.basket_1.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.get(reverse('detail-basket', kwargs={'basket_id':basket_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_basket_detail_forbidden(self):
        basket_id = self.basket_1.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.get(reverse('detail-basket', kwargs={'basket_id':basket_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_basket_detail_not_found(self):
        response = self.client.get(reverse('detail-basket', kwargs={'basket_id': 123}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_basket_detail(self):
        basket_id = self.basket_1.data.get('id')
        response = self.client.get(reverse('detail-basket', kwargs={'basket_id':basket_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_basket_delete_un_auth(self):
        basket_id = self.basket_1.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION='')
        response = self.client.delete(reverse('detail-basket', kwargs={'basket_id':basket_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_basket_delete_forbidden(self):
        basket_id = self.basket_1.data.get('id')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.delete(reverse('detail-basket', kwargs={'basket_id':basket_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_basket_delete_not_found(self):
        response = self.client.delete(reverse('detail-basket', kwargs={'basket_id': 123}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_basket_delete(self):
        basket_id = self.basket_1.data.get('id')
        response = self.client.delete(reverse('detail-basket', kwargs={'basket_id':basket_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)