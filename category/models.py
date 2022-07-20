from django.db import models


class Category(models.Model):
	title = models.CharField(verbose_name='Название', max_length=255, unique=True)
	is_active = models.BooleanField(default=True)

	class Meta:
		verbose_name = 'Категория'
		verbose_name_plural = 'Категории'

	def __str__(self):
		return self.title