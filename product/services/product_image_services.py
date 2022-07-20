from product.models import ProductImage
from product.services.func import path_image_for_product
from base_services import write_image


class ProductImageService:

	def add_images_for_product(self, product,  product_images):
		for image in product_images:
			image_path = path_image_for_product(instance=product,filename=image)
			ProductImage.objects.create(product=product,image=image_path)
			write_image(image=image, image_path=image_path)
		return product



		