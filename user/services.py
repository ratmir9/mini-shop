from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import status

from user.serializers import (
	UserSerializer,
	RegistrationSerializer
)
from base_services import detail_obj


class UserService:
	def get_users_by_id(self, id):
		try:
			return User.objects.get(id=id)
		except User.DoesNotExist:
			return ""

	def get_detail_user(self, id):
		user = self.get_users_by_id(id)
		if not user:
			return Response(user, status.HTTP_404_NOT_FOUND)
		return detail_obj(
			serializer_class=UserSerializer,
			obj=user,
			status_code=status.HTTP_200_OK,
		)

	def list_users(self):
		users = User.objects.all()
		return detail_obj(
			serializer_class=UserSerializer,
			obj=users,
			status_code=status.HTTP_200_OK,
			many=True
		)

	def check_is_owner_or_is_admin(self, user, owner):
		return bool(user == owner or owner.is_staff)

	def create_user(self, user_data):
		serializer = RegistrationSerializer(data=user_data)
		if serializer.is_valid():
			
			user = serializer.save()
			return detail_obj(
				serializer_class=UserSerializer,
				obj=user,
				status_code=status.HTTP_201_CREATED
			)
			# return Response(serializer.data, status.HTTP_201_CREATED)
		return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

	def delete_user(self, user_id, owner):
		user = self.get_users_by_id(user_id)
		if not user:
			return Response(user, status.HTTP_404_NOT_FOUND)
		if not self.check_is_owner_or_is_admin(user, owner):
			return Response({"msg": "you don't have access"}, status.HTTP_403_FORBIDDEN)
		user.delete()
		return detail_obj(
			serializer_class=UserSerializer,
			obj=user,
			status_code=status.HTTP_204_NO_CONTENT
		) 
		
