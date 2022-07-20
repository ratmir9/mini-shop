from django.urls import path

from category.views import (
	CategoryAPIView, 
	CategoryDetailAPIView, 
	ProductInCategoryAPIView
)


urlpatterns = [
	path('<int:id>/products/', ProductInCategoryAPIView.as_view()),
	path('<int:category_id>/', CategoryDetailAPIView.as_view(), name='detail-category'),
	path('', CategoryAPIView.as_view(), name='categories')
]