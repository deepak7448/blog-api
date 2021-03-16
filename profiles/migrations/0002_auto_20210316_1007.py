# Generated by Django 3.1.7 on 2021-03-16 10:07

from django.db import migrations
import django_resized.forms
import profiles.models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profiles',
            name='profile_pic',
            field=django_resized.forms.ResizedImageField(crop=None, default='profile/avatar.svg', force_format='JPEG', keep_meta=True, quality=75, size=[500, 500], upload_to=profiles.models.upload_location),
        ),
    ]