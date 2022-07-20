from django.db import models


class Basket(models.Model):
	products = models.ManyToManyField(
		'product.Product', verbose_name='Товары',               
		through="ProductInBasket", through_fields=('basket', 'product')
	)
	owner = models.ForeignKey('auth.User', verbose_name='Хозяин корзины',on_delete=models.CASCADE)
	created_at = models.DateTimeField(verbose_name='Врем создания', auto_now_add=True)

	class Meta:
		verbose_name = 'Корзина'
		verbose_name_plural = 'Корзины'


class ProductInBasket(models.Model):
	basket = models.ForeignKey(Basket, on_delete=models.CASCADE)
	quantity = models.IntegerField(verbose_name='Количество', default=1)
	product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
	add_time = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ['basket', 'product']
