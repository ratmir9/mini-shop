from rest_framework.views import APIView
from rest_framework import permissions
from user.services import UserService


class UserAPIView(APIView):
	permission_classes = [permissions.IsAdminUser]
	user_service = UserService()

	def get(self, request):
		return self.user_service.list_users()


class UserDetailAPIView(APIView):
	permission_classes = [permissions.IsAuthenticatedOrReadOnly]
	user_service = UserService()

	def get(self, request, user_id):
		return self.user_service.get_detail_user(user_id)

	def delete(self, request, user_id):
		return self.user_service.delete_user(user_id, owner=request.user)


class RegisterAPIView(APIView):
	user_service = UserService()
	
	def post(self, request):
		user_data = request.data
		return self.user_service.create_user(user_data)