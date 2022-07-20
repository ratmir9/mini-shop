from django.urls import path

from order.views import (
	OrderAPIView, 
	OrderDetailAPIView
)


urlpatterns = [
	path('<int:order_id>/', OrderDetailAPIView.as_view(), name='detail-order'),
	path('', OrderAPIView.as_view(), name='orders')
]