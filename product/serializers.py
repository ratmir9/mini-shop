from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from product.models import (
	Product,
	ProductImage
)


class ProductListSerializer(serializers.ModelSerializer):
	image = serializers.SerializerMethodField('get_image_uri')
	
	class Meta:
		model = Product
		fields = '__all__'

	def get_image_uri(self, obj):
		return self.context['request'].build_absolute_uri(obj.image.url)


class ProductImageSerializer(serializers.ModelSerializer):
	image = serializers.SerializerMethodField('get_image_uri')
	
	class Meta:
		model = ProductImage
		fields = ['id', 'image']
	
	def get_image_uri(self, obj):
		return self.context['request'].build_absolute_uri(obj.image.url)


class ProdSerializer(serializers.Serializer):
	product_id = serializers.IntegerField(required=True)
	quantity = serializers.IntegerField(default=1)


class ProductDetailSerializer(serializers.ModelSerializer):
	image = serializers.SerializerMethodField('get_image_uri')
	images = ProductImageSerializer(read_only=True, many=True)
	
	class Meta:
		model = Product
		fields = ['id', 'title', 'description','image', 'images', 'price','is_active', 'created_at', 'category']
	
	def get_image_uri(self, obj):
		return self.context['request'].build_absolute_uri(obj.image.url)


class ProductCreateSerializer(serializers.ModelSerializer):
	title = serializers.CharField(
		label='Название',
		max_length=255, 
		required=True,
		validators=[
			UniqueValidator(
				queryset=Product.objects.all(), 
				message='product with this title already exists.'
			)
		]
	)
	images = serializers.ListField(child=serializers.ImageField(max_length=None), required=False)
	
	class Meta:
		model = Product
		fields = ['title', 'description', 'price','image', 'category', 'images']
		extra_kwargs = {
			'title': {'required': True},
			'description': {'required': True},
			'price': {'required': True},
			'category': {'required': True}
		}
