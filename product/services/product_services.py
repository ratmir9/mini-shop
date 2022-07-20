from rest_framework import status
from rest_framework.response import Response

from product.models import Product
from product.serializers import (
	ProductDetailSerializer,
	ProductListSerializer,
	ProductCreateSerializer
)
from product.services.product_image_services import ProductImageService
from base_services import detail_obj


class ProductService:
	product_query = Product.objects.select_related('category').prefetch_related('images')

	def _detail_product(self, product):
		serializer = ProductDetailSerializer(product)
		return Response(serializer.data)

	def get_product_by_id(self, id):
		try:
			return self.product_query.get(id=id)
		except Product.DoesNotExist:
			return ""

	def list_product(self, request):
		products = self.product_query.all()
		return detail_obj(
			serializer_class=ProductListSerializer,
			obj=products,
			status_code=status.HTTP_200_OK,
			request=request,
			many=True
		)

	def check_list_product_data(self, products):
		data = {}
		errors = []
		for product in products:
			p = self.get_product_by_id(product['product_id'])
			if not p:
				error = {'msg': f'product with {product["product_id"]} not'}
				errors.append(error)
			else:
				product['product_id'] = p
		if not errors:
			data['products'] = products
		data['errors'] = errors
		return data
		
	def add_product(self, product_data, request):
		images = []
		serializer = ProductCreateSerializer(data=product_data)
		if serializer.is_valid():
			if serializer.validated_data.get('images'):
				images = serializer.validated_data.pop('images')
			image = serializer.validated_data.pop('image')
			product = Product.objects.create(**serializer.validated_data)
			product.image = image
			product.save()
			if images:
				product = ProductImageService().add_images_for_product(product, images)
			return detail_obj(
				serializer_class=ProductDetailSerializer,
				obj=product,
				request=request,
				status_code=status.HTTP_201_CREATED
			)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
		
	def detail_product(self, request, id):
		product = self.get_product_by_id(id)
		if not product:
			return Response({'msg': f'not product with id {id}'}, status.HTTP_404_NOT_FOUND)
		return detail_obj(
			serializer_class=ProductDetailSerializer,
			obj=product,
			request=request,
			status_code=status.HTTP_200_OK
		)

	def delete_product(self, id):
		product = self.get_product_by_id(id)
		if not product:
			return Response({'msg': f'not product with id {id}'}, status.HTTP_404_NOT_FOUND)
		product.delete()
		return Response({'msg': 'success deleted'}, status.HTTP_204_NO_CONTENT)

	def products_in_category(self, category_id):
		products = (
			Product.objects.prefetch_related(self.product_query)
			.filter(category_id=category_id)
		)
		return detail_obj(
			serializer_class=ProductListSerializer,
			obj=products,
			status_code=status.HTTP_200_OK,
			many=True
		)

	def search_products(self, product_title, request):
		products = self.product_query.filter(title__icontains=product_title)
		if not products:
			return Response({'msg': ''}, status.HTTP_404_NOT_FOUND)
		return detail_obj(
			serializer_class=ProductDetailSerializer,
			obj=products,
			request=request,
			status_code=status.HTTP_200_OK,
			many=True
		)

