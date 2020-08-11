from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import ImageViewSet, DownloadView

router = DefaultRouter()
router.register('image', ImageViewSet, basename='image')

urlpatterns = [
    path('download/<str:name>', DownloadView.as_view()),
]

urlpatterns += router.urls
