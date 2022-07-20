from django.contrib.auth.models import User
from rest_framework import serializers

from order.models import Order, ProductInOrder
from product.serializers import ProductDetailSerializer, ProdSerializer


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['username']
		

class ProductInOrderSerializer(serializers.ModelSerializer):
	product = ProductDetailSerializer()
	class Meta:
		model = ProductInOrder
		fields = ['product', 'quantity']
		extra_kwargs = {'quantity': {'required': True}}
		

class OrderSerializer(serializers.ModelSerializer):
	products = ProductInOrderSerializer(many=True, source="productinorder_set")

	class Meta:
		model = Order
		fields = ['id', 'username', 'phone', 'products', 'total_amount', 'total_quantity_product']
		depth = 1 


class OrderCreateSerializer(serializers.ModelSerializer):
	products = ProdSerializer(many=True)
	class Meta:
		model = Order
		fields = ['username', 'phone', 'products']

	def products_validate(self, value):
		if not value:
			raise serializers.ValidationError('пожалуйста добавьте товары')

	