from rest_framework.views import APIView

from category.permissions import IsAdminOrReadOnly
from category.services import CategoryService


class CategoryAPIView(APIView):
	permission_classes = [IsAdminOrReadOnly]
	category_service = CategoryService()

	def get(self, request):
		return self.category_service.list_categories()

	def post(self, request):
		return self.category_service.add_category(data=request.data)


class CategoryDetailAPIView(APIView):
	permission_classes = [IsAdminOrReadOnly]
	category_service = CategoryService()

	def get(self, request, category_id):
		return self.category_service.detail_category(category_id)

	def put(self, request, category_id):
		return self.category_service.change_category(category_id, category_data=request.data)

	def delete(self, request, category_id):
		return self.category_service.delete_category(category_id)


class ProductInCategoryAPIView(APIView):
	category_service = CategoryService()
	
	def get(self, request, id):
		return self.category_service.list_product_by_category_id(id)