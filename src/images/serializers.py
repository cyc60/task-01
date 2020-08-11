from rest_framework import serializers

from .models import Image, Annotation, ImageSurface, ImageClass
from .fields import Base64ImageField


class ShapeSerializer(serializers.Serializer):
    startX = serializers.FloatField(required=False)
    startY = serializers.FloatField(required=False)
    endX = serializers.FloatField(required=False)
    endY = serializers.FloatField(required=False)

    class Meta:
        fields = ('startX', 'startY', 'endX', 'endY')


class AnnotationSerializer(serializers.Serializer):
    shape = ShapeSerializer(required=False)
    meta = serializers.JSONField(required=False)
    class_id = serializers.CharField(required=False, source='image_class.name')
    surface = serializers.ListField(
        child=serializers.CharField(min_length=1, max_length=256),
        allow_empty=False,
        required=False,
        write_only=True
    )

    class Meta:
        fields = ('shape', 'meta', 'class_id', 'surface')

    def to_representation(self, instance):
        resp = super().to_representation(instance)
        resp['surface'] = [x.name for x in instance.surface.all()]
        resp['shape'] = {
            'startX': instance.startX,
            'startY': instance.startY,
            'endX': instance.endX,
            'endY': instance.endY,
        }
        return resp


class ImageCreateSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=True, write_only=True)
    annotation = AnnotationSerializer(required=False, write_only=True)

    class Meta:
        model = Image
        fields = ('image', 'annotation', 'id')

    def create(self, validated_data):
        annotation_data = validated_data.pop('annotation', {})
        image = super().create(validated_data)

        annotation = Annotation.objects.create(
            image=image,
            meta=annotation_data.get('meta'),
            startX=annotation_data.get('shape', {}).get('startX'),
            startY=annotation_data.get('shape', {}).get('startY'),
            endX=annotation_data.get('shape', {}).get('endX'),
            endY=annotation_data.get('shape', {}).get('endY'),
        )
        if annotation_data.get('image_class'):
            image_class, _ = ImageClass.objects.get_or_create(name=annotation_data.get('image_class').get('name'))
            annotation.image_class = image_class
            annotation.save(update_fields=['image_class'])

        if annotation_data.get('surface'):
            for surface_name in annotation_data.get('surface'):
                surface_item, _ = ImageSurface.objects.get_or_create(name=surface_name)
                annotation.surface.add(surface_item)

        return image


class ImageUpdateSerializer(serializers.ModelSerializer):
    annotation = AnnotationSerializer(required=True)

    class Meta:
        model = Image
        fields = ('annotation', )

    def update(self, instance, validated_data):
        annotation_data = validated_data.pop('annotation', {})

        image = super().update(instance, validated_data)

        annotation, _ = Annotation.objects.update_or_create(image=image)
        if annotation_data.get('meta'):
            annotation.meta = annotation_data.get('meta')
        if annotation_data.get('shape'):
            annotation.startX = annotation_data.get('shape', {}).get('startX')
            annotation.startY = annotation_data.get('shape', {}).get('startY')
            annotation.endX = annotation_data.get('shape', {}).get('endX')
            annotation.endY = annotation_data.get('shape', {}).get('endY')
        if annotation_data.get('image_class'):
            image_class, _ = ImageClass.objects.get_or_create(name=annotation_data.get('image_class').get('name'))
            annotation.image_class = image_class

        annotation.save()

        if annotation_data.get('surface'):
            annotation.surface.clear()
            for surface_name in annotation_data.get('surface'):
                surface_item, _ = ImageSurface.objects.get_or_create(name=surface_name)
                annotation.surface.add(surface_item)

        return image


class ImageInternalSerializer(serializers.ModelSerializer):
    meta = serializers.JSONField(source='annotation.meta')
    shape = ShapeSerializer(source='annotation')
    class_id = serializers.CharField(source='annotation.image_class.name', allow_null=True)
    surface = serializers.StringRelatedField(source='annotation.surface', many=True)

    class Meta:
        model = Image
        fields = ('id', 'meta', 'shape', 'class_id', 'surface')


class LabelsInternalSerializer(serializers.Serializer):
    labels = ImageInternalSerializer(many=True)

    class Meta:
        fields = ('labels',)


class ImageExportSerializer(serializers.ModelSerializer):
    class_id = serializers.CharField(source='annotation.image_class.name')
    surface = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ('id', 'class_id', 'surface')

    def get_surface(self, obj):
        if hasattr(obj, 'annotation'):
            return ''.join([x.name for x in obj.annotation.surface.all()])


class LabelsExportSerializer(serializers.Serializer):
    labels = ImageExportSerializer(many=True)

    class Meta:
        fields = ('labels',)
