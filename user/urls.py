from django.urls import path
from user.views import UserAPIView, UserDetailAPIView, RegisterAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
	path('register/', RegisterAPIView.as_view(), name='register'),
	path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
	path('<int:user_id>/', UserDetailAPIView.as_view(), name='detail-user'),
	path('', UserAPIView.as_view(), name='users')	
]