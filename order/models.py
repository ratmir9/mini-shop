from django.db import models


class Order(models.Model):
	products = models.ManyToManyField(
		'product.Product', verbose_name='Товары',
		through="ProductInOrder", through_fields=('order', 'product')
	)
	username = models.CharField(verbose_name='Имя заказчика', max_length=255)
	phone = models.CharField(verbose_name='Номер телефона', max_length=15)
	total_amount = models.DecimalField(
		verbose_name='Общая сумма заказа', blank=True,
		null='True', max_digits=9, decimal_places=2, editable=False
	)
	total_quantity_product = models.PositiveSmallIntegerField(
		verbose_name='Обшее количество товаров',
		blank=True, null=True, editable=False
	)
	owner = models.ForeignKey('auth.User',verbose_name='Владелец корзины' ,on_delete=models.CASCADE)
	created_at = models.DateTimeField(verbose_name='Время заказа', auto_now_add=True)

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'
	

class ProductInOrder(models.Model):
	order = models.ForeignKey('order.Order', on_delete=models.CASCADE)
	product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
	quantity = models.PositiveSmallIntegerField(default=1)
