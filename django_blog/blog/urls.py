from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView, LoginView
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    add_comment,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    path('home', views.home, name="home"),
    path("login/", LoginView.as_view(template_name="blog/login.html"), name="login"),
    path("register/", views.register, name="register"),
    path('logout/', LogoutView.as_view(template_name="blog/logout.html"), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path("posts/", PostListView.as_view(), name="posts"),  # Keep "posts" for your list template
    path("post/new/", PostCreateView.as_view(), name="post_create"),  # Checker compliance
    path("post/<int:pk>/", PostDetailView.as_view(), name="post_detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post_update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post_delete"),
    path("posts/<int:post_id>/comments/new/", add_comment, name="add_comment"),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment_edit"),
    path("comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment_delete"),
]

