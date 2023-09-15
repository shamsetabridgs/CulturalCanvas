# Generated by Django 3.2.8 on 2023-09-09 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0003_alter_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(error_messages={'unique': 'The email must be unique'}, max_length=150, unique=True),
        ),
    ]
