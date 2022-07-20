import os
import shutil

from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, override_settings
from rest_framework import status

from category.models import Category
from base_services import get_access_token


class CategoryTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user_1', password='1234pass')
        self.access_token_for_user = get_access_token(self.user)
        self.superuser = User.objects.create_superuser(username='superuser', password='1234pass')
        self.access_token_for_superuser = get_access_token(self.superuser)
        self.data = {
            'title': 'Category 1',
            'is_active': True
        }
        self.category_1 = Category.objects.create(**self.data)

    def test_category_list(self):
        response = self.client.get(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_create_un_auth(self):
        response = self.client.post(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_create_forbidden(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.post(reverse('categories'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_create(self):
        self.data['title'] = 'Product 2'
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_superuser)
        response = self.client.post(reverse('categories'), self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_category_detail_not_found(self):
        response = self.client.get(reverse('detail-category', kwargs={'category_id':123}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_detail(self):
        category_id = self.category_1.id
        response = self.client.get(reverse('detail-category', kwargs={'category_id': category_id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_change_un_auth(self):
        category_id = self.category_1.id
        response = self.client.put(reverse('detail-category', kwargs={'category_id': category_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_change_forbidden(self):
        category_id = self.category_1.id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.put(reverse('detail-category', kwargs={'category_id': category_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_change(self):
        self.data['title'] = 'Category 123'
        category_id = self.category_1.id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_superuser)
        response = self.client.put(reverse('detail-category', kwargs={'category_id': category_id}), self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_category_delete_un_auth(self):
        category_id = self.category_1.id
        response = self.client.delete(reverse('detail-category', kwargs={'category_id': category_id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_category_delete_forbidden(self):
        category_id = self.category_1.id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_user)
        response = self.client.delete(reverse('detail-category', kwargs={'category_id': category_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_category_delete_not_found(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_superuser)
        response = self.client.delete(reverse('detail-category', kwargs={'category_id': 1234})) 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_category_delete(self):
        category_id = self.category_1.id
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token_for_superuser)
        response = self.client.delete(reverse('detail-category', kwargs={'category_id': category_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)