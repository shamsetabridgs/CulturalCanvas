# Generated by Django 3.2.8 on 2023-09-02 11:53

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0008_auto_20230902_1139'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='views',
            field=models.ManyToManyField(related_name='post_views', to=settings.AUTH_USER_MODEL),
        ),
    ]
