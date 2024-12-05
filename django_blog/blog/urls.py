from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name="home" ),
    path("login", views.login, name="login"),
    path("posts", views.posts, name= "posts"),
    path("register", views.register, name="register"),
]