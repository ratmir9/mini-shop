from django.db.models import Prefetch
from rest_framework import status
from rest_framework.response import Response

from order.models import (
	Order,
	ProductInOrder
)
from order.serializers import (
	OrderSerializer,
	OrderCreateSerializer
)
from product.services.product_services import ProductService
from product.services.product_services import ProductService
from base_services import (
	check_is_owner_or_is_admin,
	detail_obj
)


class OrderService:
	product_in_order = Prefetch(
		'productinorder_set',
		ProductInOrder.objects.select_related('product', 'product__category')
		.prefetch_related('product__images')
	)

	def _add_product_in_order(self, order, products):
		for product in products:
			order.products.add(
				product.get('product_id'),
				through_defaults={'quantity': product.get('quantity')}
			)
			order.save()
		return order
	
	def create_order(self, order_data, owner, request):
		serializer = OrderCreateSerializer(data=order_data)
		if serializer.is_valid():
			products = serializer.validated_data.pop('products')
			products_data = ProductService().check_list_product_data(products)
			if products_data.get('errors'):
				return Response(products_data.get('errors'))
			products = products_data.get('products')
			total_amount, total_quantity_product = self.calculation_amount_amd_quantity(products)
			order = Order.objects.create(
				**serializer.validated_data,
				total_quantity_product=total_quantity_product,
				total_amount=total_amount, 
				owner=owner
			)
			order = self._add_product_in_order(order, products)
			return detail_obj(
				serializer_class=OrderSerializer,
				obj=order,
				request=request,
				status_code=status.HTTP_201_CREATED
			)
		else:
			return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)	

	def get_order_by_id(self, order_id):
		try:
			order = ( 
			Order.objects.prefetch_related(self.product_in_order)
			.get(id=order_id)
		)
		except Order.DoesNotExist:
			return ""
		return order

	def calculation_amount_amd_quantity(self, products):
		total_amount = 0
		total_quantity_product = 0
		for product in products:
			total_amount += product['product_id'].price * product.get('quantity', 1)
			total_quantity_product += product.get('quantity', 1)
		return total_amount, total_quantity_product

	def list_order(self, request):
		orders = ( 
			Order.objects.prefetch_related(self.product_in_order)
			.all()
		)
		return detail_obj(
			serializer_class=OrderSerializer,
			obj=orders,
			request=request,
			status_code=status.HTTP_200_OK,
			many=True
		)	

	def detail_order(self, order_id, owner, request):
		order = self.get_order_by_id(order_id)
		if not order:
			return Response(order, status.HTTP_404_NOT_FOUND)		
		if not check_is_owner_or_is_admin(order, owner):
			return Response({"msg": "you don't have access"}, status.HTTP_403_FORBIDDEN)
		return detail_obj(
			serializer_class=OrderSerializer,
			obj=order,
			request=request,
			status_code=status.HTTP_200_OK
		)

	def delete_order(self, order_id, owner):
		order = self.get_order_by_id(order_id)
		if not order:
			return Response(order, status.HTTP_404_NOT_FOUND)
		if not check_is_owner_or_is_admin(order, owner):
			return Response({"msg": "you don't have access"}, status.HTTP_403_FORBIDDEN)
		order.delete()
		return Response({'msg': 'success'}, status.HTTP_204_NO_CONTENT)
		

