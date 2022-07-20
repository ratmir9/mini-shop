import os
import shutil

from django.db.models.signals import post_delete
from django.dispatch import receiver

from product.models import Product


@receiver(post_delete, sender=Product)
def delete_directory_images(sender, instance, **kwargs):
	path = instance.image.path
	path = '/'.join(path.split('/')[0:-1])
	if os.path.exists(path):
		shutil.rmtree(path)