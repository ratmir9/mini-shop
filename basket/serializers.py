from rest_framework import serializers
from basket.models import Basket, ProductInBasket
from product.serializers import ProdSerializer, ProductDetailSerializer


class ProductInBasketSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = ProductInBasket
		fields = ['product', 'quantity',  'add_time']


class ProductInBasketDetailSerializer(serializers.ModelSerializer):
	product = ProductDetailSerializer()
	
	class Meta:
		model = ProductInBasket
		fields = ['product', 'quantity', 'add_time']
		depth = 1


class BasketListSerializer(serializers.ModelSerializer):
	products = ProductInBasketSerializer(many=True, source="productinbasket_set")
	
	class Meta:
		model = Basket
		fields = ['id', 'owner', 'products', 'created_at']

class BasketDetailSerializer(serializers.ModelSerializer):
	products = ProductInBasketDetailSerializer(many=True, source="productinbasket_set")
	
	class Meta:
		model = Basket
		fields = ['id', 'owner', 'products', 'created_at']


class BasketCreateSerializer(serializers.ModelSerializer):
	products = ProdSerializer(many=True)
	
	class Meta:
		model = Basket
		fields = ['products']

	def validate_products(self, value):
		if not value:
			raise serializers.ValidationError('пожалуйста добавьте товары')
	

