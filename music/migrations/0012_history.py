# Generated by Django 4.1.5 on 2023-01-31 03:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('music', '0011_image_vip_remove_review_movie_remove_review_parent_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_stories', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to=settings.AUTH_USER_MODEL)),
                ('history', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stories', to='music.musicinfo')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
