import os
import mimetypes

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets, mixins

from .serializers import ImageCreateSerializer, ImageUpdateSerializer, LabelsInternalSerializer, LabelsExportSerializer
from .models import Image


class ImageViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):

    queryset = Image.objects.all()

    def get_serializer_class(self):
        if self.action in ['create']:
            serializer_class = ImageCreateSerializer
        elif self.action in ['update', 'partial_update']:
            serializer_class = ImageUpdateSerializer
        else:
            serializer_class = super().get_serializer_class()

        return serializer_class

    def list(self, request, *args, **kwargs):
        if request.query_params.get('format') == 'export':
            queryset = Image.objects.confirmed()
            serializer = LabelsExportSerializer({'labels': queryset})
        else:
            queryset = Image.objects.all()
            serializer = LabelsInternalSerializer({'labels': queryset})

        return Response(serializer.data)


class DownloadView(APIView):
    def get(self, request, name, format=None):
        image = get_object_or_404(Image, image=name)
        image_buffer = open(image.image.path, "rb").read()
        content_type = mimetypes.guess_type(str(image.image.file))[0]
        response = HttpResponse(image_buffer, content_type=content_type)
        response['Content-Disposition'] = 'inline; filename="%s"' % os.path.basename(image.image.path)
        return response
