from django.contrib import admin
from django.urls import (
    path, 
    include
)
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/baskets/', include('basket.urls')),
    path('api/v1/categories/', include('category.urls')),
    path('api/v1/orders/', include('order.urls')),
    path('api/v1/products/', include('product.urls')),
    path('api/v1/users/', include('user.urls')),    
    path('__debug__/', include('debug_toolbar.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

