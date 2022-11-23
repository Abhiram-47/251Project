from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class list(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="todolist",null=True)
    def __str__(self):
        return self.name


class item(models.Model):
    l = models.ForeignKey(list, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    checked = models.BooleanField()

    def __str__(self):
        return self.text

class Movie(models.Model):
    title=models.CharField(max_length=100,null=True)
    plot=models.CharField(max_length=1000)
    language=models.CharField(max_length=100)
    Director=models.CharField(max_length=100,null=True)
    Producer=models.CharField(max_length=100,null=True)
    Writer=models.CharField(max_length=100,null=True)
    year=models.CharField(max_length=1000)
    duration=models.CharField(max_length=100)
    genre=models.CharField(max_length=100)
    rating=models.CharField(max_length=100)
    platform =models.JSONField(default='{}')
    cast=models.JSONField(default='{}')
    image=models.CharField(max_length=100000,null=True)
    users_wishlist=models.ManyToManyField(User, related_name="users_wishlist", blank=True)
    users_favlist=models.ManyToManyField(User, related_name="users_fav", blank=True)
    users_watchedlist=models.ManyToManyField(User, related_name="users_watchedlist", blank=True)

    def _str_(self):
        return self.year