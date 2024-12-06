from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('home', views.home, name="home" ),
    path("login/", LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("posts", views.posts, name= "posts"),
    path("register/", views.register, name="register"),
    path('logout', LogoutView.as_view(next_page = "/"), name="logout"),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]