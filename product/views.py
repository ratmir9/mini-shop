from rest_framework.views import APIView

from product.services.product_services import ProductService
from product.permissions import IsAdminOrReadOnly


class ProductAPIView(APIView):
	permission_classes = [IsAdminOrReadOnly]
	product_service = ProductService()
	
	def get(self, request):
		if request.GET.get('title'):
			title = request.GET.get('title')
			return self.product_service.search_products(title, request=request)
		return self.product_service.list_product(request=request)

	def post(self, request):
		product_data = request.data
		return self.product_service.add_product(product_data, request=request)


class ProductDetailAPIView(APIView):
	permission_classes = [IsAdminOrReadOnly]
	product_service = ProductService()
	
	def get(self, request, product_id):
		return self.product_service.detail_product(id=product_id, request=request)

	def delete(self, request, product_id):
		return self.product_service.delete_product(product_id)
