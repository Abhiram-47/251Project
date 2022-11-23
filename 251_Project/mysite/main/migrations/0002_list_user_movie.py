# Generated by Django 4.1.2 on 2022-11-23 00:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='todolist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, null=True)),
                ('plot', models.CharField(max_length=1000)),
                ('language', models.CharField(max_length=100)),
                ('Director', models.CharField(max_length=100, null=True)),
                ('Producer', models.CharField(max_length=100, null=True)),
                ('Writer', models.CharField(max_length=100, null=True)),
                ('year', models.CharField(max_length=1000)),
                ('duration', models.CharField(max_length=100)),
                ('genre', models.CharField(max_length=100)),
                ('rating', models.CharField(max_length=100)),
                ('platform', models.JSONField(default='{}')),
                ('cast', models.JSONField(default='{}')),
                ('image', models.CharField(max_length=100000, null=True)),
                ('users_favlist', models.ManyToManyField(blank=True, related_name='users_fav', to=settings.AUTH_USER_MODEL)),
                ('users_watchedlist', models.ManyToManyField(blank=True, related_name='users_watchedlist', to=settings.AUTH_USER_MODEL)),
                ('users_wishlist', models.ManyToManyField(blank=True, related_name='users_wishlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
