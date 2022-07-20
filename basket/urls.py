from django.urls import path
from basket.views import (
	BasketAPIView, 
	BasketDetailAPIView
)


urlpatterns = [
	path('<int:basket_id>/', BasketDetailAPIView.as_view(), name='detail-basket'),
	path('', BasketAPIView.as_view(), name='baskets')
]