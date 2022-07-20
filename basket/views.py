from rest_framework.views import APIView
from rest_framework import permissions

from basket.services import BasketService
from basket.permissions import IsAuthenticatedOrAdminReadOnly


class BasketAPIView(APIView):
	permission_classes = [IsAuthenticatedOrAdminReadOnly]
	basket_service = BasketService()


	def get(self, request):
		return self.basket_service.get_list_basket(request=request)
	
	def post(self, request):
		return self.basket_service.add_product_in_basket(
			data=request.data,
			owner_id=request.user.pk,
			request=request
		)
		
class BasketDetailAPIView(APIView):
	permission_classes = [permissions.IsAuthenticated]
	basket_service = BasketService()
	
	def get(self, request, basket_id):
		return self.basket_service.detail_basket(
			basket_id, owner=request.user, request=request
		)

	def delete(self, request, basket_id):
		return self.basket_service.delete_basket(
			basket_id, owner=request.user
		)
