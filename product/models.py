from django.db import models

from category.models import Category
from product.services.func import path_image_for_product


class Product(models.Model):
	title = models.CharField(verbose_name='Название', max_length=255,  unique=True)
	description = models.TextField(verbose_name='Описание')
	price = models.DecimalField(verbose_name='Цена', max_digits=8, decimal_places=2)
	image = models.ImageField(verbose_name='Изображение', upload_to=path_image_for_product)
	category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
	is_active = models.BooleanField(verbose_name='Опубликована',default=True)
	created_at = models.DateTimeField(verbose_name='Время публикации', auto_now_add=True)

	class Meta:
		verbose_name = 'Товар'
		verbose_name_plural = 'Товары'

	def __str__(self):
		return f'Название: {self.title}'


class ProductImage(models.Model):
	product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
	image = models.ImageField(verbose_name='Изображение')

	class Meta:
		verbose_name = 'Изображение товара'
		verbose_name_plural = 'Изображения товара'

