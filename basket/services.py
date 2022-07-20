from django.db.models import Prefetch
from rest_framework.response import Response
from rest_framework import status

from basket.models import (
	Basket, 
	ProductInBasket
)
from basket.serializers import (
	BasketCreateSerializer, 
	BasketDetailSerializer
)
from product.services.product_services import ProductService
from base_services import (
	detail_obj,
	check_is_owner_or_is_admin
)


class BasketService():
	product_in_basket = Prefetch(
		'productinbasket_set',
		ProductInBasket.objects.select_related('product', 'product__category')
		.prefetch_related('product__images')
	)

	def _detail_basket(self, basket):
		serializer = BasketDetailSerializer(basket)
		return Response(serializer.data)

	def _add_product_in_basket(self, basket,products):
		for product in products:
			basket.products.add(
				product['product_id'],
				through_defaults={'quantity': product.get('quantity', 1)}
			)
			basket.save()
		return basket

	def get_basket_by_id(self, basket_id):
		try:
			basket = (
				Basket.objects.prefetch_related(self.product_in_basket)
				.get(id=basket_id)
			)
		except Basket.DoesNotExist:
			return ""
		return basket
	
	def check_basket_for_owner(self, owner_id):
		try:
			return Basket.objects.get(owner_id=owner_id)
		except Basket.DoesNotExist:
			return ""

	def add_product_in_basket(self, data, owner_id, request):
		serializer = BasketCreateSerializer(data=data)
		if serializer.is_valid():
			products = data.pop('products')
			products_data = ProductService().check_list_product_data(products)
			if products_data.get('errors'):
				return Response(products_data.get('errors'), status.HTTP_400_BAD_REQUEST)	
			products = products_data.get('products')
		else:
			return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
		basket_owner = self.check_basket_for_owner(owner_id)
		if not basket_owner:
			basket_owner = Basket.objects.create(owner_id=owner_id)
		basket = self._add_product_in_basket(basket_owner, products)
		return detail_obj(
			serializer_class=BasketDetailSerializer,
			obj=basket,
			request=request,
			status_code=status.HTTP_201_CREATED
		)

	def get_list_basket(self, request):
		baskets = (
			Basket.objects.prefetch_related(self.product_in_basket)
			.all()
		)
		return detail_obj(
			serializer_class=BasketDetailSerializer,
			obj=baskets,
			request=request,
			status_code=status.HTTP_200_OK,
			many=True
		)
	
	def detail_basket(self, basket_id, owner, request):
		basket = self.get_basket_by_id(basket_id)
		if not basket:
			return Response(basket, status.HTTP_404_NOT_FOUND)
		if not check_is_owner_or_is_admin(basket, owner):
			return Response({"msg": "you don't have access"}, status.HTTP_403_FORBIDDEN)
		return detail_obj(
			serializer_class=BasketDetailSerializer,
			obj=basket,
			request=request,
			status_code=status.HTTP_200_OK
		)
	
	def delete_basket(self, basket_id, owner):
		basket = self.get_basket_by_id(basket_id)
		if not basket:
			return Response(basket, status.HTTP_404_NOT_FOUND)
		if not check_is_owner_or_is_admin(basket, owner):
			return Response({"msg": "you don't have access"}, status.HTTP_403_FORBIDDEN)
		basket.delete()
		return Response({'msg' : 'success'}, status.HTTP_204_NO_CONTENT)