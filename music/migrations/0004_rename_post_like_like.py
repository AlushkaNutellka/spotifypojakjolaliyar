# Generated by Django 4.1.4 on 2023-01-26 03:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0003_musicinfo_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='post',
            new_name='like',
        ),
    ]