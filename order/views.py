from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from order.services import OrderService
from order.permissions import IsAuthenticatedOrAdminReadOnly


class OrderAPIView(APIView):
	permission_classes = [IsAuthenticatedOrAdminReadOnly]
	order_service = OrderService()
	
	def get(self, request):
		return self.order_service.list_order(request)

	def post(self, request):
		order_data = request.data
		return self.order_service.create_order(
			order_data, owner=request.user, request=request
		)


class OrderDetailAPIView(APIView):
	permission_classes = [IsAuthenticated]
	order_service = OrderService()

	def get(self, request, order_id):
		return self.order_service.detail_order(
			order_id, owner=request.user, request=request
		)

	def delete(self, request, order_id):
		return self.order_service.delete_order(
			order_id, owner=request.user
		)