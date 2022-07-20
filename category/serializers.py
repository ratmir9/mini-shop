from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from category.models import Category


class CategorySerializer(serializers.ModelSerializer):
	class Meta:
		model = Category
		fields = ['id','title', 'is_active']


class CategoryCreateSerializer(serializers.ModelSerializer):
	title = serializers.CharField(
		label='Название',
		max_length=255, 
		required=True,
		validators=[
			UniqueValidator(
				queryset=Category.objects.all(), 
				message='category with this title already exists.'
			)
		]
	)
	
	class Meta:
		model = Category
		fields = ['title', 'is_active']
