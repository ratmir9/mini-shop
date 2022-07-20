from django.urls import path

from product.views import (
	ProductAPIView,
	ProductDetailAPIView
)


urlpatterns = [
	path('<int:product_id>/', ProductDetailAPIView.as_view(), name='detail-product'),
	path('', ProductAPIView.as_view(), name='products')
]