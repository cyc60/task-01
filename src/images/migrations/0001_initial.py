# Generated by Django 3.1 on 2020-08-11 02:25

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ImageSurface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Annotation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meta', models.JSONField(blank=True, null=True)),
                ('startY', models.FloatField(blank=True, null=True)),
                ('startX', models.FloatField(blank=True, null=True)),
                ('endX', models.FloatField(blank=True, null=True)),
                ('endY', models.FloatField(blank=True, null=True)),
                ('image', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='annotation', to='images.image')),
                ('image_class', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='images.imageclass')),
                ('surface', models.ManyToManyField(blank=True, to='images.ImageSurface')),
            ],
        ),
    ]
