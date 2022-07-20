import io
import os
from django.conf import settings
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from PIL import Image


def generate_image():
    file = io.BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file


def get_access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def detail_obj(serializer_class, obj, status_code, request=None, many=False):
    if not request:
        serializer = serializer_class(instance=obj, many=many)
    serializer = serializer_class(instance=obj, context={'request': request}, many=many)
    return Response(serializer.data, status=status_code)


def check_is_owner_or_is_admin(obj, owner):
	return bool(obj.owner == owner or owner.is_staff)

def write_image(image, image_path):
	image_path = os.path.join(settings.MEDIA_ROOT, image_path)
	with open(image_path, 'wb+') as file:
		for chunk in image.chunks():
			file.write(chunk)
