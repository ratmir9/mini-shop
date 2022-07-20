import os
import uuid


def path_image_for_product(instance, filename):
	prefix = str(uuid.uuid4()).split('-')[-1]
	file = f'{prefix}_{filename}'
	category = f'category_{instance.category.id}'
	product = f'product_{instance.id}'
	path = os.path.join(category, product, file)
	return path
	

