from django.urls import path
from . import views

app_name="main"
urlpatterns=[
    path("",views.start,name="start"),
    path("home/",views.home,name="home"),
    path("index/",views.index,name="index"),
    #path("<int:id>",views.li,name="list"),
    path("create/",views.create,name="create"),
    path("view/",views.view,name="view"),
    path("results/",views.results,name="results"),
    path("<int:id>",views.cinema,name="movie"),

    # Wish list
    path("wishlist/", views.wishlist, name="wishlist"),
    path("wishlist/add_to_wishlist/<int:id>", views.add_to_wishlist, name="user_wishlist"),
    # Fav list
    path("favlist/", views.favlist, name="favlist"),
    path("favlist/add_to_favlist/<int:id>", views.add_to_favlist, name="user_favlist"),
    # Watched list
    path("watchedlist/", views.watchedlist, name="watchedlist"),
    path("watchedlist/add_to_watchedlist/<int:id>", views.add_to_watchedlist, name="user_watchedlist"),



]