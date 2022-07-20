from rest_framework import status
from rest_framework.response import Response

from category.models import Category
from category.serializers import CategorySerializer, CategoryCreateSerializer
from product.services.product_services import ProductService
from base_services import detail_obj


class CategoryService:
	def _get_category_by_id(self, id: int):
		try:
			return Category.objects.get(pk=id)
		except Category.DoesNotExist:
			return ""
	
	def detail_category(self, id):
		category = self._get_category_by_id(id)
		if not category:
			return Response("", status.HTTP_404_NOT_FOUND)
		return detail_obj(
			serializer_class=CategorySerializer,	
			obj=category,
			status_code=status.HTTP_200_OK
		)

	def list_categories(self):
		categories = Category.objects.all()
		return detail_obj(
			serializer_class=CategorySerializer,
			obj=categories,
			status_code=status.HTTP_200_OK,
			many=True
		)
	
	def add_category(self, data):
		serializer = CategoryCreateSerializer(data=data)
		if serializer.is_valid():
			category = Category.objects.create(**serializer.validated_data)
			return detail_obj(
				serializer_class=CategorySerializer,
				obj=category,
				status_code=status.HTTP_201_CREATED
			)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def change_category(self, id, category_data):
		category = self._get_category_by_id(id)
		if not category:
			return Response({'msg':f'категории с {id} нет'}, status.HTTP_404_NOT_FOUND)
		serializer = CategorySerializer(category, data=category_data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status.HTTP_200_OK)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def list_product_by_category_id(self, id):
		return ProductService().products_in_category(category_id=id)

	def delete_category(self, id):
		category = self._get_category_by_id(id)
		if not category:
			return Response(category, status.HTTP_404_NOT_FOUND)
		category.delete()
		return Response({'msg': 'success'}, status.HTTP_204_NO_CONTENT)




