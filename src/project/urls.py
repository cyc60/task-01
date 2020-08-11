from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import images.urls as api_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include((api_urls, 'images'), namespace='api-v1')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
